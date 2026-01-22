import argparse
import os
from typing import Optional, Tuple

from api.db import get_conn


def env_flag(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "y"}


def resolve_active_week(conn, data_version: str, requested_week: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    with conn.cursor() as cur:
        if requested_week:
            cur.execute(
                """
                SELECT week, active_id
                FROM tech_progress_scope_active
                WHERE data_version = %s
                  AND week = %s
                  AND status = 'active'
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (data_version, requested_week),
            )
        else:
            cur.execute(
                """
                SELECT week, active_id
                FROM tech_progress_scope_active
                WHERE data_version = %s
                  AND status = 'active'
                ORDER BY week DESC, created_at DESC
                LIMIT 1
                """,
                (data_version,),
            )
        row = cur.fetchone()
        if row:
            return row[0], row[1]
    return None, None


def main():
    parser = argparse.ArgumentParser(description="Aggregate occupation AI scores")
    parser.add_argument(
        "--data-version",
        default=os.getenv("ONET_DATA_VERSION")
        or os.getenv("DEFAULT_DATA_VERSION")
        or "30.1",
        help="O*NET data version label",
    )
    parser.add_argument(
        "--week",
        default=os.getenv("TECH_PROGRESS_WEEK"),
        help="Tech progress week (YYYY-Www). Defaults to latest active scope week.",
    )
    parser.add_argument("--verbose", action="store_true", default=env_flag("AGG_VERBOSE", "0"))
    args = parser.parse_args()

    with get_conn() as conn:
        week, active_id = resolve_active_week(conn, args.data_version, args.week)
        if not week or not active_id:
            print(
                "[agg] no active scope",
                f"data_version={args.data_version}",
                f"week={args.week or 'latest'}",
                flush=True,
            )
            return
        with conn.cursor() as cur:
            if args.verbose:
                print(
                    "[agg] start",
                    f"data_version={args.data_version}",
                    f"week={week}",
                    f"active_id={active_id}",
                    flush=True,
                )
            cur.execute(
                """
                INSERT INTO occupation_ai_score (
                    data_version, week, soc_code,
                    mean, std,
                    ai_augmentation_potential_mean, ai_augmentation_potential_std,
                    human_context_dependency_mean, human_context_dependency_std,
                    physical_world_dependency_mean, physical_world_dependency_std,
                    confidence_mean, confidence_std,
                    updated_at
                )
                SELECT
                    otw.data_version,
                    %(week)s AS week,
                    otw.soc_code,
                    SUM(otw.weight * tae.mean) AS mean,
                    SQRT(SUM(POWER(otw.weight * COALESCE(tae.std, 0), 2))) AS std,
                    SUM(otw.weight * tae.ai_augmentation_potential_mean) AS ai_augmentation_potential_mean,
                    SQRT(SUM(POWER(otw.weight * COALESCE(tae.ai_augmentation_potential_std, 0), 2))) AS ai_augmentation_potential_std,
                    SUM(otw.weight * tae.human_context_dependency_mean) AS human_context_dependency_mean,
                    SQRT(SUM(POWER(otw.weight * COALESCE(tae.human_context_dependency_std, 0), 2))) AS human_context_dependency_std,
                    SUM(otw.weight * tae.physical_world_dependency_mean) AS physical_world_dependency_mean,
                    SQRT(SUM(POWER(otw.weight * COALESCE(tae.physical_world_dependency_std, 0), 2))) AS physical_world_dependency_std,
                    SUM(otw.weight * tae.confidence_mean) AS confidence_mean,
                    SQRT(SUM(POWER(otw.weight * COALESCE(tae.confidence_std, 0), 2))) AS confidence_std,
                    NOW()
                FROM occupation_task_weight otw
                JOIN task_ai_ensemble tae
                  ON tae.data_version = otw.data_version
                 AND tae.task_id = otw.task_id
                 AND tae.week = %(week)s
                WHERE otw.data_version = %(data_version)s
                GROUP BY otw.data_version, otw.soc_code
                ON CONFLICT (data_version, week, soc_code) DO UPDATE
                SET mean = EXCLUDED.mean,
                    std = EXCLUDED.std,
                    ai_augmentation_potential_mean = EXCLUDED.ai_augmentation_potential_mean,
                    ai_augmentation_potential_std = EXCLUDED.ai_augmentation_potential_std,
                    human_context_dependency_mean = EXCLUDED.human_context_dependency_mean,
                    human_context_dependency_std = EXCLUDED.human_context_dependency_std,
                    physical_world_dependency_mean = EXCLUDED.physical_world_dependency_mean,
                    physical_world_dependency_std = EXCLUDED.physical_world_dependency_std,
                    confidence_mean = EXCLUDED.confidence_mean,
                    confidence_std = EXCLUDED.confidence_std,
                    updated_at = EXCLUDED.updated_at
                """,
                {"data_version": args.data_version, "week": week},
            )
            if args.verbose:
                print("[agg] done", f"rows={cur.rowcount}", flush=True)
        conn.commit()


if __name__ == "__main__":
    main()
