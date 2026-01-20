import argparse
import os

from api.db import get_conn


def env_flag(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "y"}


def main():
    parser = argparse.ArgumentParser(description="Aggregate occupation AI scores")
    parser.add_argument(
        "--data-version",
        default=os.getenv("ONET_DATA_VERSION")
        or os.getenv("DEFAULT_DATA_VERSION")
        or "30.1",
        help="O*NET data version label",
    )
    parser.add_argument("--verbose", action="store_true", default=env_flag("AGG_VERBOSE", "0"))
    args = parser.parse_args()

    with get_conn() as conn:
        with conn.cursor() as cur:
            if args.verbose:
                print("[agg] start", f"data_version={args.data_version}", flush=True)
            cur.execute(
                """
                INSERT INTO occupation_ai_score (data_version, soc_code, mean, std, updated_at)
                SELECT
                    otw.data_version,
                    otw.soc_code,
                    SUM(otw.weight * tae.mean) AS mean,
                    SQRT(SUM(POWER(otw.weight * COALESCE(tae.std, 0), 2))) AS std,
                    NOW()
                FROM occupation_task_weight otw
                JOIN task_ai_ensemble tae
                  ON tae.data_version = otw.data_version
                 AND tae.task_id = otw.task_id
                WHERE otw.data_version = %s
                GROUP BY otw.data_version, otw.soc_code
                ON CONFLICT (data_version, soc_code) DO UPDATE
                SET mean = EXCLUDED.mean,
                    std = EXCLUDED.std,
                    updated_at = EXCLUDED.updated_at
                """,
                (args.data_version,),
            )
            if args.verbose:
                print("[agg] done", f"rows={cur.rowcount}", flush=True)
        conn.commit()


if __name__ == "__main__":
    main()
