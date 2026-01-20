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
        "http://localhost:3000,http://127.0.0.1:3000",
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


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/occupations")
def list_occupations(
    search: Optional[str] = Query(default=None),
    sort: str = Query(default="ai"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    data_version: Optional[str] = Query(default=None),
):
    params = {}

    with get_conn() as conn:
        conn.row_factory = dict_row
        data_version = resolve_data_version(conn, data_version)

        where_clauses = ["om.onetsoc_code LIKE '%%.00'", "om.data_version = %(data_version)s"]
        params["data_version"] = data_version

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
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@app.get("/occupations/{soc_code}")
def get_occupation(soc_code: str, data_version: Optional[str] = Query(default=None)):
    with get_conn() as conn:
        conn.row_factory = dict_row
        data_version = resolve_data_version(conn, data_version)
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
                SELECT mean, std, updated_at
                FROM occupation_ai_score
                WHERE data_version = %(data_version)s
                  AND soc_code = %(soc_code)s
                """,
                {"data_version": data_version, "soc_code": soc_code},
            )
            ai_score = cur.fetchone()

    return {
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
    data_version: Optional[str] = Query(default=None),
):
    with get_conn() as conn:
        conn.row_factory = dict_row
        data_version = resolve_data_version(conn, data_version)
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
                WHERE om.data_version = %(data_version)s
                  AND om.onetsoc_code LIKE '%%.00'
                ORDER BY oai.mean DESC NULLS LAST
                LIMIT %(limit)s
                """,
                {"data_version": data_version, "limit": limit},
            )
            items = cur.fetchall()

    return {"items": items, "limit": limit}
