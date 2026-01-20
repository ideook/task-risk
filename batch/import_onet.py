import argparse
import os
from pathlib import Path
from typing import Iterable, Tuple

from api.db import get_conn
from batch.utils import copy_rows, iter_insert_rows


def iter_occupation_rows(file_path: str, data_version: str) -> Iterable[Tuple]:
    for row in iter_insert_rows(file_path, "occupation_data"):
        onetsoc_code = row.get("onetsoc_code")
        title = row.get("title")
        description = row.get("description")
        soc_code = onetsoc_code[:7] if onetsoc_code else None
        yield (data_version, onetsoc_code, soc_code, title, description)


def iter_alternate_title_rows(file_path: str, data_version: str) -> Iterable[Tuple]:
    for row in iter_insert_rows(file_path, "alternate_titles"):
        yield (
            data_version,
            row.get("onetsoc_code"),
            row.get("alternate_title"),
            row.get("short_title"),
        )


def iter_task_statement_rows(file_path: str, data_version: str) -> Iterable[Tuple]:
    seen = set()
    for row in iter_insert_rows(file_path, "task_statements"):
        task_id_raw = row.get("task_id")
        if task_id_raw is None:
            continue
        task_id = int(float(task_id_raw))
        if task_id in seen:
            continue
        seen.add(task_id)
        yield (data_version, task_id, row.get("task"))


def iter_task_rating_rows(file_path: str, data_version: str) -> Iterable[Tuple]:
    for row in iter_insert_rows(file_path, "task_ratings"):
        task_id_raw = row.get("task_id")
        task_id = int(float(task_id_raw)) if task_id_raw is not None else None
        yield (
            data_version,
            row.get("onetsoc_code"),
            task_id,
            row.get("scale_id"),
            _to_int(row.get("category")),
            _to_float(row.get("data_value")),
            _to_int(row.get("n")),
            _to_float(row.get("standard_error")),
            _to_float(row.get("lower_ci_bound")),
            _to_float(row.get("upper_ci_bound")),
            row.get("recommend_suppress"),
            row.get("date_updated"),
            row.get("domain_source"),
        )


def _to_int(value):
    if value is None:
        return None
    return int(float(value))


def _to_float(value):
    if value is None:
        return None
    return float(value)


def main():
    parser = argparse.ArgumentParser(description="Import core O*NET tables")
    parser.add_argument(
        "--sql-dir",
        default=os.getenv("ONET_SQL_DIR", "./Data/db_30_1_mysql"),
        help="Path to O*NET MySQL SQL files",
    )
    parser.add_argument(
        "--mode",
        choices=["truncate"],
        default="truncate",
        help="Reload strategy",
    )
    parser.add_argument(
        "--data-version",
        default=os.getenv("ONET_DATA_VERSION")
        or os.getenv("DEFAULT_DATA_VERSION")
        or "30.1",
        help="O*NET data version label (e.g., 30.1)",
    )
    args = parser.parse_args()

    sql_dir = args.sql_dir
    if not os.path.isabs(sql_dir):
        repo_root = Path(__file__).resolve().parents[1]
        sql_dir = str((repo_root / sql_dir).resolve())

    occupation_file = os.path.join(sql_dir, "03_occupation_data.sql")
    alternate_file = os.path.join(sql_dir, "29_alternate_titles.sql")
    task_statements_file = os.path.join(sql_dir, "17_task_statements.sql")
    task_ratings_file = os.path.join(sql_dir, "18_task_ratings.sql")
    data_version = args.data_version

    with get_conn() as conn:
        conn.autocommit = False
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO data_version (id, is_active)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (data_version, False),
            )
            if args.mode == "truncate":
                cur.execute(
                    """
                    DELETE FROM occupation_ai_score WHERE data_version = %s;
                    DELETE FROM task_ai_ensemble WHERE data_version = %s;
                    DELETE FROM task_ai_score WHERE data_version = %s;
                    DELETE FROM occupation_task_ratings WHERE data_version = %s;
                    DELETE FROM alternate_titles WHERE data_version = %s;
                    DELETE FROM task_catalog WHERE data_version = %s;
                    DELETE FROM occupation_task_weight WHERE data_version = %s;
                    DELETE FROM task_statements WHERE data_version = %s;
                    DELETE FROM occupation_master WHERE data_version = %s;
                    """
                    ,
                    (
                        data_version,
                        data_version,
                        data_version,
                        data_version,
                        data_version,
                        data_version,
                        data_version,
                        data_version,
                        data_version,
                    ),
                )
        conn.commit()

        copy_rows(
            conn,
            "occupation_master",
            ["data_version", "onetsoc_code", "soc_code", "title", "description"],
            iter_occupation_rows(occupation_file, data_version),
        )

        copy_rows(
            conn,
            "alternate_titles",
            ["data_version", "onetsoc_code", "alternate_title", "short_title"],
            iter_alternate_title_rows(alternate_file, data_version),
        )

        copy_rows(
            conn,
            "task_statements",
            ["data_version", "task_id", "task_statement"],
            iter_task_statement_rows(task_statements_file, data_version),
        )

        copy_rows(
            conn,
            "occupation_task_ratings",
            [
                "data_version",
                "onetsoc_code",
                "task_id",
                "scale_id",
                "category",
                "data_value",
                "n",
                "standard_error",
                "lower_ci_bound",
                "upper_ci_bound",
                "recommend_suppress",
                "date_updated",
                "domain_source",
            ],
            iter_task_rating_rows(task_ratings_file, data_version),
        )
        conn.commit()


if __name__ == "__main__":
    main()
