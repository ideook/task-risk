import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from psycopg.rows import dict_row

from api.db import get_conn

app = FastAPI(title="task-risk")

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOW_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://192.168.3.91:3000,"
        "http://localhost:3001,http://127.0.0.1:3001,http://192.168.3.91:3001",
    ).split(",")
    if origin.strip()
]
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def resolve_data_version(conn, requested: Optional[str]) -> str:
    if requested:
        return requested
    env_version = os.getenv("DEFAULT_DATA_VERSION")
    if env_version:
        return env_version
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id
            FROM data_version
            WHERE is_active = TRUE
            ORDER BY id DESC
            LIMIT 1
            """
        )
        row = cur.fetchone()
        if row:
            return row[0]
    return "30.1"


def resolve_week(conn, data_version: str, requested: Optional[str]) -> Optional[str]:
    if requested:
        return requested
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT week
            FROM tech_progress_weekly_snapshot
            WHERE data_version = %(data_version)s
            ORDER BY week DESC
            LIMIT 1
            """,
            {"data_version": data_version},
        )
        row = cur.fetchone()
        if row:
            return row["week"]
    return None


def resolve_active_week(conn, data_version: str, requested: Optional[str]) -> Optional[str]:
    if requested:
        return requested
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT week
            FROM tech_progress_scope_active
            WHERE data_version = %(data_version)s
              AND status = 'active'
            ORDER BY week DESC, created_at DESC
            LIMIT 1
            """,
            {"data_version": data_version},
        )
        row = cur.fetchone()
        if row:
            return row["week"] if isinstance(row, dict) else row[0]
    return None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/occupations")
def list_occupations(
    search: Optional[str] = Query(default=None),
    sort: str = Query(default="ai"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    week: Optional[str] = Query(default=None),
    data_version: Optional[str] = Query(default=None),
):
    params = {}

    with get_conn() as conn:
        conn.row_factory = dict_row
        data_version = resolve_data_version(conn, data_version)
        score_week = resolve_active_week(conn, data_version, week)

        where_clauses = ["om.onetsoc_code LIKE '%%.00'", "om.data_version = %(data_version)s"]
        params["data_version"] = data_version
        params["week"] = score_week

        if search:
            where_clauses.append("(om.title ILIKE %(q)s OR om.soc_code ILIKE %(q)s)")
            params["q"] = f"%{search}%"

        where_sql = ""
        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)

        if sort == "employment":
            order_sql = "ORDER BY bls.employment DESC NULLS LAST"
        else:
            order_sql = "ORDER BY oai.mean DESC NULLS LAST"

        offset = (page - 1) * page_size
        params.update({"limit": page_size, "offset": offset})

        query = f"""
            SELECT
                om.onetsoc_code,
                om.soc_code,
                om.title,
                oai.mean AS ai_mean,
                oai.std AS ai_std,
                bls.employment,
                bls.median_wage,
                bls.ref_year_month
            FROM occupation_master om
            LEFT JOIN occupation_ai_score oai
              ON oai.data_version = om.data_version
             AND oai.soc_code = om.soc_code
             AND (
               (%(week)s::text IS NULL AND oai.week = 'legacy')
               OR oai.week = %(week)s::text
             )
            LEFT JOIN (
                SELECT DISTINCT ON (soc_code)
                    soc_code, ref_year_month, employment, median_wage
                FROM bls_oews_metrics
                ORDER BY soc_code, ref_year_month DESC
            ) bls ON bls.soc_code = om.soc_code
            {where_sql}
            {order_sql}
            LIMIT %(limit)s OFFSET %(offset)s
        """

        count_query = f"""
            SELECT COUNT(*) AS total
            FROM occupation_master om
            {where_sql}
        """

        with conn.cursor() as cur:
            cur.execute(query, params)
            items = cur.fetchall()
            cur.execute(count_query, params)
            total = cur.fetchone()["total"]

    return {
        "week": score_week,
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@app.get("/occupations/{soc_code}")
def get_occupation(
    soc_code: str,
    week: Optional[str] = Query(default=None),
    data_version: Optional[str] = Query(default=None),
):
    with get_conn() as conn:
        conn.row_factory = dict_row
        data_version = resolve_data_version(conn, data_version)
        score_week = resolve_active_week(conn, data_version, week)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT onetsoc_code, title, description
                FROM occupation_master
                WHERE data_version = %(data_version)s
                  AND soc_code = %(soc_code)s
                ORDER BY onetsoc_code
                """,
                {"data_version": data_version, "soc_code": soc_code},
            )
            rows = cur.fetchall()

            if not rows:
                raise HTTPException(status_code=404, detail="occupation not found")

            onetsoc_codes = [row["onetsoc_code"] for row in rows]
            title = rows[0]["title"]
            description = rows[0]["description"]

            cur.execute(
                """
                SELECT DISTINCT alternate_title
                FROM alternate_titles
                WHERE data_version = %(data_version)s
                  AND onetsoc_code = ANY(%(codes)s)
                ORDER BY alternate_title
                """,
                {"data_version": data_version, "codes": onetsoc_codes},
            )
            alternate_titles = [row["alternate_title"] for row in cur.fetchall()]

            cur.execute(
                """
                SELECT ts.task_id, ts.task_statement, otw.weight
                FROM occupation_task_weight otw
                JOIN task_statements ts
                  ON ts.data_version = otw.data_version
                 AND ts.task_id = otw.task_id
                WHERE otw.data_version = %(data_version)s
                  AND otw.soc_code = %(soc_code)s
                ORDER BY otw.weight DESC
                LIMIT 20
                """,
                {"data_version": data_version, "soc_code": soc_code},
            )
            top_tasks = cur.fetchall()

            cur.execute(
                """
                SELECT
                  mean,
                  std,
                  ai_augmentation_potential_mean,
                  ai_augmentation_potential_std,
                  human_context_dependency_mean,
                  human_context_dependency_std,
                  physical_world_dependency_mean,
                  physical_world_dependency_std,
                  confidence_mean,
                  confidence_std,
                  updated_at
                FROM occupation_ai_score
                WHERE data_version = %(data_version)s
                  AND soc_code = %(soc_code)s
                  AND (
                    (%(week)s::text IS NULL AND week = 'legacy')
                    OR week = %(week)s::text
                  )
                """,
                {"data_version": data_version, "soc_code": soc_code, "week": score_week},
            )
            ai_score = cur.fetchone()

    return {
        "week": score_week,
        "soc_code": soc_code,
        "onetsoc_codes": onetsoc_codes,
        "title": title,
        "description": description,
        "alternate_titles": alternate_titles,
        "top_tasks": top_tasks,
        "ai_score": ai_score,
    }


@app.get("/rankings/ai_risk")
def ai_risk_rankings(
    limit: int = Query(default=50, ge=1, le=200),
    week: Optional[str] = Query(default=None),
    data_version: Optional[str] = Query(default=None),
):
    with get_conn() as conn:
        conn.row_factory = dict_row
        data_version = resolve_data_version(conn, data_version)
        score_week = resolve_active_week(conn, data_version, week)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    om.soc_code,
                    om.title,
                    oai.mean AS ai_mean,
                    oai.std AS ai_std
                FROM occupation_master om
                JOIN occupation_ai_score oai
                  ON oai.data_version = om.data_version
                 AND oai.soc_code = om.soc_code
                 AND (
                   (%(week)s::text IS NULL AND oai.week = 'legacy')
                   OR oai.week = %(week)s::text
                 )
                WHERE om.data_version = %(data_version)s
                  AND om.onetsoc_code LIKE '%%.00'
                ORDER BY oai.mean DESC NULLS LAST
                LIMIT %(limit)s
                """,
                {"data_version": data_version, "limit": limit, "week": score_week},
            )
            items = cur.fetchall()

    return {"week": score_week, "items": items, "limit": limit}


@app.get("/tech-progress/weeks")
def list_tech_progress_weeks(
    data_version: Optional[str] = Query(default=None),
):
    with get_conn() as conn:
        conn.row_factory = dict_row
        data_version = resolve_data_version(conn, data_version)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT DISTINCT week
                FROM tech_progress_weekly_snapshot
                WHERE data_version = %(data_version)s
                ORDER BY week DESC
                """,
                {"data_version": data_version},
            )
            weeks = [row["week"] for row in cur.fetchall()]
    return {"data_version": data_version, "weeks": weeks}


@app.get("/tech-progress/summary")
def tech_progress_summary(
    week: Optional[str] = Query(default=None),
    data_version: Optional[str] = Query(default=None),
):
    with get_conn() as conn:
        conn.row_factory = dict_row
        data_version = resolve_data_version(conn, data_version)
        resolved_week = resolve_week(conn, data_version, week)

        if not resolved_week:
            return {
                "data_version": data_version,
                "week": None,
                "active_scope_id": None,
                "tasks_with_change": 0,
                "avg_progress": None,
                "top_tasks": [],
                "top_tech": [],
            }

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT active_id
                FROM tech_progress_scope_active
                WHERE data_version = %(data_version)s
                  AND week = %(week)s
                  AND status = 'active'
                ORDER BY created_at DESC
                LIMIT 1
                """,
                {"data_version": data_version, "week": resolved_week},
            )
            active_row = cur.fetchone()
            active_id = active_row["active_id"] if active_row else None

            if not active_id:
                return {
                    "data_version": data_version,
                    "week": resolved_week,
                    "active_scope_id": None,
                    "tasks_with_change": 0,
                    "avg_progress": None,
                    "top_tasks": [],
                    "top_tech": [],
                }

            cur.execute(
                """
                WITH scope_tasks AS (
                  SELECT task_id
                  FROM tech_progress_scope_active_task
                  WHERE active_id = %(active_id)s
                    AND data_version = %(data_version)s
                ),
                snap AS (
                  SELECT s.progress_score, s.delta
                  FROM tech_progress_weekly_snapshot s
                  JOIN scope_tasks st ON st.task_id = s.task_id
                  WHERE s.data_version = %(data_version)s
                    AND s.week = %(week)s
                )
                SELECT
                  COUNT(*) FILTER (WHERE delta <> 0) AS tasks_with_change,
                  AVG(progress_score) AS avg_progress
                FROM snap
                """,
                {
                    "active_id": active_id,
                    "data_version": data_version,
                    "week": resolved_week,
                },
            )
            metrics = cur.fetchone() or {}

            cur.execute(
                """
                WITH scope_tasks AS (
                  SELECT task_id
                  FROM tech_progress_scope_active_task
                  WHERE active_id = %(active_id)s
                    AND data_version = %(data_version)s
                )
                SELECT s.task_id, ts.task_statement, s.delta
                FROM tech_progress_weekly_snapshot s
                JOIN scope_tasks st ON st.task_id = s.task_id
                JOIN task_statements ts
                  ON ts.data_version = %(data_version)s
                 AND ts.task_id = s.task_id
                WHERE s.data_version = %(data_version)s
                  AND s.week = %(week)s
                ORDER BY s.delta DESC NULLS LAST
                LIMIT 6
                """,
                {
                    "active_id": active_id,
                    "data_version": data_version,
                    "week": resolved_week,
                },
            )
            top_tasks = cur.fetchall()

            cur.execute(
                """
                WITH scope_tasks AS (
                  SELECT task_id
                  FROM tech_progress_scope_active_task
                  WHERE active_id = %(active_id)s
                    AND data_version = %(data_version)s
                )
                SELECT
                  l.tech_id,
                  t.name,
                  COUNT(DISTINCT l.task_id) AS task_count,
                  AVG(l.impact_score) AS avg_impact
                FROM tech_progress_task_link l
                JOIN tech_progress_technology t ON t.tech_id = l.tech_id
                JOIN scope_tasks st ON st.task_id = l.task_id
                WHERE l.data_version = %(data_version)s
                  AND l.week = %(week)s
                GROUP BY l.tech_id, t.name
                ORDER BY task_count DESC, avg_impact DESC
                LIMIT 6
                """,
                {
                    "active_id": active_id,
                    "data_version": data_version,
                    "week": resolved_week,
                },
            )
            top_tech = cur.fetchall()

    return {
        "data_version": data_version,
        "week": resolved_week,
        "active_scope_id": active_id,
        "tasks_with_change": metrics.get("tasks_with_change", 0),
        "avg_progress": metrics.get("avg_progress"),
        "top_tasks": top_tasks,
        "top_tech": top_tech,
    }


@app.get("/tech-progress/tasks")
def list_tech_progress_tasks(
    week: Optional[str] = Query(default=None),
    data_version: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    link_type: Optional[str] = Query(default=None),
    min_delta: Optional[float] = Query(default=None),
):
    with get_conn() as conn:
        conn.row_factory = dict_row
        data_version = resolve_data_version(conn, data_version)
        resolved_week = resolve_week(conn, data_version, week)

        if not resolved_week:
            return {
                "data_version": data_version,
                "week": None,
                "items": [],
                "page": page,
                "page_size": page_size,
                "total": 0,
            }

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT active_id
                FROM tech_progress_scope_active
                WHERE data_version = %(data_version)s
                  AND week = %(week)s
                  AND status = 'active'
                ORDER BY created_at DESC
                LIMIT 1
                """,
                {"data_version": data_version, "week": resolved_week},
            )
            active_row = cur.fetchone()
            active_id = active_row["active_id"] if active_row else None

            if not active_id:
                return {
                    "data_version": data_version,
                    "week": resolved_week,
                    "items": [],
                    "page": page,
                    "page_size": page_size,
                    "total": 0,
                }

            offset = (page - 1) * page_size
            params = {
                "active_id": active_id,
                "data_version": data_version,
                "week": resolved_week,
                "limit": page_size,
                "offset": offset,
                "link_type": link_type,
                "min_delta": min_delta,
            }

            cur.execute(
                """
                WITH scope_tasks AS (
                  SELECT task_id
                  FROM tech_progress_scope_active_task
                  WHERE active_id = %(active_id)s
                    AND data_version = %(data_version)s
                )
                SELECT
                  s.task_id,
                  ts.task_statement,
                  s.progress_score,
                  s.delta,
                  top_tech.tech_id AS top_tech_id,
                  top_tech.tech_name AS top_tech_name,
                  COALESCE(link_counts.link_count, 0) AS link_count
                FROM tech_progress_weekly_snapshot s
                JOIN scope_tasks st ON st.task_id = s.task_id
                JOIN task_statements ts
                  ON ts.data_version = %(data_version)s
                 AND ts.task_id = s.task_id
                LEFT JOIN LATERAL (
                  SELECT l.tech_id, t.name AS tech_name
                  FROM tech_progress_task_link l
                  JOIN tech_progress_technology t ON t.tech_id = l.tech_id
                  WHERE l.data_version = %(data_version)s
                    AND l.week = s.week
                    AND l.task_id = s.task_id
                  ORDER BY l.impact_score DESC
                  LIMIT 1
                ) top_tech ON TRUE
                LEFT JOIN LATERAL (
                  SELECT COUNT(*) AS link_count
                  FROM tech_progress_task_link l2
                  WHERE l2.data_version = %(data_version)s
                    AND l2.week = s.week
                    AND l2.task_id = s.task_id
                ) link_counts ON TRUE
                WHERE s.data_version = %(data_version)s
                  AND s.week = %(week)s
                  AND (
                    %(min_delta)s::double precision IS NULL
                    OR s.delta >= %(min_delta)s::double precision
                  )
                  AND (
                    %(link_type)s::text IS NULL OR EXISTS (
                      SELECT 1
                      FROM tech_progress_task_link l3
                      WHERE l3.data_version = s.data_version
                        AND l3.week = s.week
                        AND l3.task_id = s.task_id
                        AND l3.link_type = %(link_type)s::text
                    )
                  )
                ORDER BY s.delta DESC NULLS LAST
                LIMIT %(limit)s OFFSET %(offset)s
                """,
                params,
            )
            items = cur.fetchall()

            cur.execute(
                """
                WITH scope_tasks AS (
                  SELECT task_id
                  FROM tech_progress_scope_active_task
                  WHERE active_id = %(active_id)s
                    AND data_version = %(data_version)s
                )
                SELECT COUNT(*) AS total
                FROM tech_progress_weekly_snapshot s
                JOIN scope_tasks st ON st.task_id = s.task_id
                WHERE s.data_version = %(data_version)s
                  AND s.week = %(week)s
                  AND (
                    %(min_delta)s::double precision IS NULL
                    OR s.delta >= %(min_delta)s::double precision
                  )
                  AND (
                    %(link_type)s::text IS NULL OR EXISTS (
                      SELECT 1
                      FROM tech_progress_task_link l3
                      WHERE l3.data_version = s.data_version
                        AND l3.week = s.week
                        AND l3.task_id = s.task_id
                        AND l3.link_type = %(link_type)s::text
                    )
                  )
                """,
                params,
            )
            total = cur.fetchone()["total"]

    return {
        "data_version": data_version,
        "week": resolved_week,
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@app.get("/tech-progress/tasks/{task_id}")
def tech_progress_task_detail(
    task_id: int,
    week: Optional[str] = Query(default=None),
    data_version: Optional[str] = Query(default=None),
):
    with get_conn() as conn:
        conn.row_factory = dict_row
        data_version = resolve_data_version(conn, data_version)
        resolved_week = resolve_week(conn, data_version, week)

        if not resolved_week:
            raise HTTPException(status_code=404, detail="no tech progress data")

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT s.task_id, ts.task_statement, s.progress_score, s.delta
                FROM tech_progress_weekly_snapshot s
                JOIN task_statements ts
                  ON ts.data_version = %(data_version)s
                 AND ts.task_id = s.task_id
                WHERE s.data_version = %(data_version)s
                  AND s.week = %(week)s
                  AND s.task_id = %(task_id)s
                """,
                {
                    "data_version": data_version,
                    "week": resolved_week,
                    "task_id": task_id,
                },
            )
            task_row = cur.fetchone()
            if not task_row:
                raise HTTPException(status_code=404, detail="task not found")

            cur.execute(
                """
                SELECT
                  l.tech_id,
                  t.name AS tech_name,
                  l.link_type,
                  l.impact_score,
                  l.confidence,
                  l.evidence_id
                FROM tech_progress_task_link l
                JOIN tech_progress_technology t ON t.tech_id = l.tech_id
                WHERE l.data_version = %(data_version)s
                  AND l.week = %(week)s
                  AND l.task_id = %(task_id)s
                ORDER BY l.impact_score DESC
                """,
                {
                    "data_version": data_version,
                    "week": resolved_week,
                    "task_id": task_id,
                },
            )
            links = cur.fetchall()

            evidence_ids = list({link["evidence_id"] for link in links})
            evidence = []
            if evidence_ids:
                cur.execute(
                    """
                    SELECT
                      e.evidence_id,
                      e.evidence_date,
                      e.summary,
                      es.source_type
                    FROM tech_progress_evidence e
                    JOIN tech_progress_evidence_source es
                      ON es.source_id = e.source_id
                    WHERE e.evidence_id = ANY(%(ids)s)
                    ORDER BY e.evidence_date DESC
                    """,
                    {"ids": evidence_ids},
                )
                evidence = cur.fetchall()

    return {
        "data_version": data_version,
        "week": resolved_week,
        "task": task_row,
        "links": links,
        "evidence": evidence,
    }
