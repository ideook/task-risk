import argparse
import os
import sys

from api.db import get_conn


def main():
    parser = argparse.ArgumentParser(description="Smoke checks for task-risk data")
    parser.add_argument(
        "--data-version",
        default=os.getenv("ONET_DATA_VERSION")
        or os.getenv("DEFAULT_DATA_VERSION")
        or "30.1",
        help="O*NET data version label",
    )
    parser.add_argument("--require-ai", action="store_true", help="Require AI scores")
    args = parser.parse_args()

    failures = []

    with get_conn() as conn:
        with conn.cursor() as cur:
            def check_count(label: str, sql: str, params, minimum: int = 1):
                cur.execute(sql, params)
                count = cur.fetchone()[0]
                print(f"{label}: {count}")
                if count < minimum:
                    failures.append(f"{label} < {minimum}")

            check_count(
                "occupation_master",
                "SELECT COUNT(*) FROM occupation_master WHERE data_version = %s",
                (args.data_version,),
            )
            check_count(
                "task_statements",
                "SELECT COUNT(*) FROM task_statements WHERE data_version = %s",
                (args.data_version,),
            )
            check_count(
                "occupation_task_ratings",
                "SELECT COUNT(*) FROM occupation_task_ratings WHERE data_version = %s",
                (args.data_version,),
            )
            check_count(
                "task_catalog",
                "SELECT COUNT(*) FROM task_catalog WHERE data_version = %s",
                (args.data_version,),
            )

            if args.require_ai:
                check_count(
                    "task_ai_score",
                    "SELECT COUNT(*) FROM task_ai_score WHERE data_version = %s",
                    (args.data_version,),
                )
                check_count(
                    "occupation_ai_score",
                    "SELECT COUNT(*) FROM occupation_ai_score WHERE data_version = %s",
                    (args.data_version,),
                )
            else:
                cur.execute(
                    "SELECT COUNT(*) FROM task_ai_score WHERE data_version = %s",
                    (args.data_version,),
                )
                print(f"task_ai_score: {cur.fetchone()[0]}")
                cur.execute(
                    "SELECT COUNT(*) FROM occupation_ai_score WHERE data_version = %s",
                    (args.data_version,),
                )
                print(f"occupation_ai_score: {cur.fetchone()[0]}")

    if failures:
        print("FAILED:")
        for item in failures:
            print(f"- {item}")
        sys.exit(1)

    print("OK")


if __name__ == "__main__":
    main()
