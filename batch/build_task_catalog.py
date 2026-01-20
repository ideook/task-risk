import argparse
import os

from api.db import get_conn


def main():
    parser = argparse.ArgumentParser(description="Build task catalog")
    parser.add_argument("--size", type=int, default=int(os.getenv("TASK_CATALOG_SIZE", "200")))
    parser.add_argument("--scale-id", default="IM")
    parser.add_argument("--mode", choices=["truncate"], default="truncate")
    parser.add_argument(
        "--data-version",
        default=os.getenv("ONET_DATA_VERSION")
        or os.getenv("DEFAULT_DATA_VERSION")
        or "30.1",
        help="O*NET data version label",
    )
    args = parser.parse_args()

    with get_conn() as conn:
        with conn.cursor() as cur:
            if args.mode == "truncate":
                cur.execute(
                    "DELETE FROM task_catalog WHERE data_version = %s",
                    (args.data_version,),
                )

            cur.execute(
                """
                INSERT INTO task_catalog (data_version, task_id, score, source_scale_id)
                SELECT
                    %(data_version)s,
                    task_id,
                    AVG(data_value) AS score,
                    %(scale_id)s
                FROM occupation_task_ratings
                WHERE data_version = %(data_version)s
                  AND scale_id = %(scale_id)s
                  AND data_value IS NOT NULL
                GROUP BY task_id
                ORDER BY AVG(data_value) DESC NULLS LAST
                LIMIT %(limit)s
                """,
                {"data_version": args.data_version, "scale_id": args.scale_id, "limit": args.size},
            )
        conn.commit()


if __name__ == "__main__":
    main()
