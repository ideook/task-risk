import argparse
import os

from api.db import get_conn


def main():
    parser = argparse.ArgumentParser(description="Build occupation task weights")
    parser.add_argument("--scale-id", default="IM")
    parser.add_argument(
        "--all-tasks",
        action="store_true",
        help="Include all tasks instead of only the catalog",
    )
    parser.add_argument("--mode", choices=["truncate"], default="truncate")
    parser.add_argument(
        "--data-version",
        default=os.getenv("ONET_DATA_VERSION")
        or os.getenv("DEFAULT_DATA_VERSION")
        or "30.1",
        help="O*NET data version label",
    )
    args = parser.parse_args()

    catalog_filter = ""
    if not args.all_tasks:
        catalog_filter = "AND otr.task_id IN (SELECT task_id FROM task_catalog WHERE data_version = %(data_version)s)"

    with get_conn() as conn:
        with conn.cursor() as cur:
            if args.mode == "truncate":
                cur.execute(
                    "DELETE FROM occupation_task_weight WHERE data_version = %s",
                    (args.data_version,),
                )

            cur.execute(
                f"""
                WITH base AS (
                    SELECT
                        om.data_version,
                        om.soc_code,
                        otr.task_id,
                        otr.data_value
                    FROM occupation_task_ratings otr
                    JOIN occupation_master om
                      ON om.data_version = otr.data_version
                     AND om.onetsoc_code = otr.onetsoc_code
                    WHERE om.data_version = %(data_version)s
                      AND otr.data_version = %(data_version)s
                      AND otr.scale_id = %(scale_id)s
                      AND otr.data_value IS NOT NULL
                      {catalog_filter}
                ),
                totals AS (
                    SELECT data_version, soc_code, SUM(data_value) AS total
                    FROM base
                    GROUP BY data_version, soc_code
                )
                INSERT INTO occupation_task_weight (data_version, soc_code, task_id, weight)
                SELECT
                    b.data_version,
                    b.soc_code,
                    b.task_id,
                    b.data_value / NULLIF(t.total, 0)
                FROM base b
                JOIN totals t ON t.data_version = b.data_version AND t.soc_code = b.soc_code
                WHERE t.total IS NOT NULL
                """,
                {"data_version": args.data_version, "scale_id": args.scale_id},
            )
        conn.commit()


if __name__ == "__main__":
    main()
