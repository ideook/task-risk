import hashlib
import json
import os
from typing import List, Optional, Tuple

from api.db import get_conn

DEFAULT_TECH = [
    ("TECH-LLM-001", "LLM Response Drafting", "NLP", ["drafting", "response assistant"], "active"),
    ("TECH-TRI-001", "Ticket Triage Classifier", "NLP", ["triage", "classification"], "active"),
    ("TECH-OCR-001", "Document OCR Extractor", "Document AI", ["ocr", "document parsing"], "active"),
]

DEFAULT_SOURCES = [
    ("SRC-REL-001", "Vendor Release Notes", "product_release", None, 0.70),
    ("SRC-PAPER-001", "Research Paper", "paper", None, 0.85),
    ("SRC-REPO-001", "Open-source Repo", "repo", None, 0.60),
]

DEFAULT_EVIDENCE = [
    ("E2026W03-001", "SRC-REL-001", "2026-01-13", "Release improves response drafting accuracy for support workflows.", 0.78, "rel-2026-01-13"),
    ("E2026W03-002", "SRC-PAPER-001", "2026-01-15", "Study shows automatic triage reduces handling time with minimal error.", 0.82, "paper-2026-01-15"),
    ("E2026W04-001", "SRC-REPO-001", "2026-01-20", "OCR update improves table extraction for scanned forms.", 0.66, "repo-2026-01-20"),
    ("E2026W04-002", "SRC-REL-001", "2026-01-21", "Updated classifier reduces false positives for routing.", 0.74, "rel-2026-01-21"),
    ("E2026W05-001", "SRC-PAPER-001", "2026-01-28", "Benchmark shows better summarization for long conversations.", 0.81, "paper-2026-01-28"),
    ("E2026W06-001", "SRC-REL-001", "2026-02-03", "Routing model update improves edge-case handling.", 0.76, "rel-2026-02-03"),
]

LINK_TYPES = ["augments", "automates", "enables", "replaces"]


def _hash_int(value: str) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def _progress_score(task_id: int, week: str) -> float:
    value = _hash_int(f"progress:{week}:{task_id}") % 60
    return round(0.30 + value / 100.0, 2)


def _delta(task_id: int, week: str) -> float:
    value = _hash_int(f"delta:{week}:{task_id}") % 21
    return round((value - 10) / 100.0, 2)


def _impact(task_id: int, week: str) -> float:
    value = _hash_int(f"impact:{week}:{task_id}") % 50
    return round(0.35 + value / 100.0, 2)


def _confidence(task_id: int, week: str) -> float:
    value = _hash_int(f"conf:{week}:{task_id}") % 45
    return round(0.45 + value / 100.0, 2)


def _pick(values: List[str], idx: int) -> str:
    return values[idx % len(values)]


def _fetch_active_weeks(cur, data_version: str) -> List[Tuple[str, str]]:
    cur.execute(
        """
        SELECT week, active_id
        FROM tech_progress_scope_active
        WHERE data_version = %s
          AND status = 'active'
        ORDER BY week
        """,
        (data_version,),
    )
    return cur.fetchall()


def _fetch_task_catalog(cur, data_version: str, limit: Optional[int]) -> List[int]:
    cur.execute(
        """
        SELECT task_id
        FROM task_catalog
        WHERE data_version = %s
        ORDER BY score DESC NULLS LAST, task_id
        """,
        (data_version,),
    )
    rows = [row[0] for row in cur.fetchall()]
    return rows[:limit] if limit else rows


def _ensure_seed_data(cur):
    for tech_id, name, domain, synonyms, status in DEFAULT_TECH:
        cur.execute(
            """
            INSERT INTO tech_progress_technology (tech_id, name, domain, synonyms_json, status)
            VALUES (%s, %s, %s, %s::jsonb, %s)
            ON CONFLICT (tech_id) DO NOTHING
            """,
            (tech_id, name, domain, json.dumps(synonyms), status),
        )
    for source_id, name, source_type, base_url, trust_score in DEFAULT_SOURCES:
        cur.execute(
            """
            INSERT INTO tech_progress_evidence_source (source_id, name, source_type, base_url, trust_score)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (source_id) DO NOTHING
            """,
            (source_id, name, source_type, base_url, trust_score),
        )
    for evidence_id, source_id, evidence_date, summary, quality_score, raw_ref in DEFAULT_EVIDENCE:
        cur.execute(
            """
            INSERT INTO tech_progress_evidence (evidence_id, source_id, evidence_date, summary, quality_score, raw_ref)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (evidence_id) DO NOTHING
            """,
            (evidence_id, source_id, evidence_date, summary, quality_score, raw_ref),
        )


def regenerate(data_version: str, limit: Optional[int]) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            _ensure_seed_data(cur)
            active_weeks = _fetch_active_weeks(cur, data_version)
            if not active_weeks:
                raise SystemExit("No active tech-progress weeks found.")
            task_ids = _fetch_task_catalog(cur, data_version, limit)
            if not task_ids:
                raise SystemExit("Task catalog is empty.")

            tech_ids = [item[0] for item in DEFAULT_TECH]
            evidence_ids = [item[0] for item in DEFAULT_EVIDENCE]

            for week, active_id in active_weeks:
                cur.execute(
                    "DELETE FROM tech_progress_scope_active_task WHERE active_id = %s",
                    (active_id,),
                )
                cur.executemany(
                    """
                    INSERT INTO tech_progress_scope_active_task (active_id, week, data_version, task_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    [(active_id, week, data_version, task_id) for task_id in task_ids],
                )

                cur.execute(
                    "DELETE FROM tech_progress_task_link WHERE data_version = %s AND week = %s",
                    (data_version, week),
                )
                cur.execute(
                    "DELETE FROM tech_progress_weekly_snapshot WHERE data_version = %s AND week = %s",
                    (data_version, week),
                )
                cur.execute(
                    "DELETE FROM tech_progress_llm_task_card WHERE data_version = %s AND week = %s",
                    (data_version, week),
                )

                link_rows = []
                snapshot_rows = []
                for idx, task_id in enumerate(task_ids, start=1):
                    tech_id = _pick(tech_ids, idx)
                    link_type = _pick(LINK_TYPES, idx)
                    evidence_id = _pick(evidence_ids, idx)
                    impact_score = _impact(task_id, week)
                    confidence = _confidence(task_id, week)
                    link_rows.append(
                        (week, data_version, task_id, tech_id, link_type, impact_score, confidence, evidence_id)
                    )

                    snapshot_rows.append(
                        (
                            week,
                            data_version,
                            task_id,
                            _progress_score(task_id, week),
                            _delta(task_id, week),
                            [f"{tech_id} {link_type}"],
                            [evidence_id],
                        )
                    )

                cur.executemany(
                    """
                    INSERT INTO tech_progress_task_link (
                        week, data_version, task_id, tech_id, link_type, impact_score, confidence, evidence_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    link_rows,
                )
                cur.executemany(
                    """
                    INSERT INTO tech_progress_weekly_snapshot (
                        week, data_version, task_id, progress_score, delta, top_changes_json, evidence_ids_json
                    )
                    VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s::jsonb)
                    """,
                    [
                        (
                            week,
                            data_version,
                            task_id,
                            progress_score,
                            delta,
                            json.dumps(top_changes),
                            json.dumps(evidence_ids),
                        )
                        for week, data_version, task_id, progress_score, delta, top_changes, evidence_ids in snapshot_rows
                    ],
                )

            conn.commit()
            limit_label = limit if limit else "all"
            print(
                f"tech-progress regenerated: data_version={data_version}, weeks={len(active_weeks)}, tasks={len(task_ids)} (limit={limit_label})"
            )


if __name__ == "__main__":
    data_version = os.getenv("ONET_DATA_VERSION") or os.getenv("DEFAULT_DATA_VERSION") or "30.1"
    limit_raw = os.getenv("TECH_PROGRESS_TASK_LIMIT", "").strip()
    limit = int(limit_raw) if limit_raw else None
    regenerate(data_version, limit)
