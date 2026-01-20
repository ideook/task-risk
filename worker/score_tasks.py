import argparse
import hashlib
import json
import os
from pathlib import Path

from api.db import get_conn
from worker.llm_providers import (
    ProviderError,
    env_flag,
    get_enabled_providers,
    get_provider,
    is_provider_enabled,
    parse_model_spec,
)
from worker.retry import retry_call

PROMPT_TEMPLATE = (
    "Score the automation risk for the task below from 0 (no risk) "
    "to 100 (highly automatable). Return only the numeric score.\n\n"
    "Task: {task_statement}"
)


def hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Score tasks with LLMs (mocked by default)")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument(
        "--models",
        default="openai,claude",
        help="Comma-separated model specs (provider or provider:model)",
    )
    parser.add_argument("--prompt-version", default=os.getenv("LLM_PROMPT_VERSION", "v1"))
    parser.add_argument("--model-version", default=os.getenv("MODEL_VERSION", "mock-1"))
    parser.add_argument("--output-dir", default="worker/output")
    parser.add_argument(
        "--data-version",
        default=os.getenv("ONET_DATA_VERSION")
        or os.getenv("DEFAULT_DATA_VERSION")
        or "30.1",
        help="O*NET data version label",
    )
    parser.add_argument("--max-retries", type=int, default=int(os.getenv("LLM_MAX_RETRIES", "3")))
    parser.add_argument("--retry-base-delay", type=float, default=float(os.getenv("LLM_RETRY_BASE_DELAY", "0.5")))
    parser.add_argument("--retry-max-delay", type=float, default=float(os.getenv("LLM_RETRY_MAX_DELAY", "10.0")))
    parser.add_argument("--retry-jitter", type=float, default=float(os.getenv("LLM_RETRY_JITTER", "0.2")))
    args = parser.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data_version = args.data_version
    use_mock = env_flag("USE_MOCK_LLM", "1")
    enabled_providers = get_enabled_providers()

    model_specs = []
    for raw in models:
        try:
            model_specs.append(parse_model_spec(raw))
        except ProviderError as exc:
            print(f"[llm] skip invalid spec '{raw}': {exc}")

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tc.task_id, ts.task_statement
                FROM task_catalog tc
                JOIN task_statements ts
                  ON ts.data_version = tc.data_version
                 AND ts.task_id = tc.task_id
                WHERE tc.data_version = %(data_version)s
                ORDER BY tc.score DESC NULLS LAST
                LIMIT %(limit)s
                """,
                {"data_version": data_version, "limit": args.limit},
            )
            tasks = cur.fetchall()

        for spec in model_specs:
            model_label = spec.label
            if not is_provider_enabled(spec.provider, enabled_providers):
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO model_run (data_version, model, prompt_version, model_version, status, error_message)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            data_version,
                            model_label,
                            args.prompt_version,
                            args.model_version,
                            "skipped",
                            f"Provider disabled: {spec.provider}",
                        ),
                    )
                conn.commit()
                continue

            try:
                provider = get_provider(spec, use_mock)
            except ProviderError as exc:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO model_run (data_version, model, prompt_version, model_version, status, error_message, error_at)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW())
                        """,
                        (
                            data_version,
                            model_label,
                            args.prompt_version,
                            args.model_version,
                            "failed",
                            str(exc),
                        ),
                    )
                conn.commit()
                continue
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO model_run (data_version, model, prompt_version, model_version, status)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (data_version, model_label, args.prompt_version, args.model_version, "running"),
                )
                run_id = cur.fetchone()[0]
                conn.commit()

            prompt_hash = hash_text(
                f"{PROMPT_TEMPLATE}|{args.prompt_version}|{args.model_version}"
            )
            try:
                for task_id, task_statement in tasks:
                    input_hash = hash_text(task_statement or "")
                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            SELECT 1
                            FROM task_ai_score
                            WHERE data_version = %s
                              AND task_id = %s AND model = %s
                              AND prompt_hash = %s AND input_hash = %s
                            """,
                            (data_version, task_id, model_label, prompt_hash, input_hash),
                        )
                        if cur.fetchone():
                            continue

                    def _score_call():
                        return provider.score(
                            task_statement or "",
                            PROMPT_TEMPLATE,
                            args.prompt_version,
                            args.model_version,
                        )

                    score = retry_call(
                        _score_call,
                        retries=args.max_retries,
                        base_delay=args.retry_base_delay,
                        max_delay=args.retry_max_delay,
                        jitter=args.retry_jitter,
                    )
                    payload = {
                        "provider": spec.provider,
                        "model": spec.model,
                        "model_label": model_label,
                        "prompt_version": args.prompt_version,
                        "model_version": args.model_version,
                        "data_version": data_version,
                        "task_id": task_id,
                        "task_statement": task_statement,
                        "score": score,
                    }
                    safe_model = model_label.replace(":", "_").replace("/", "_")
                    raw_path = output_dir / f"run_{run_id}_task_{task_id}_{safe_model}.json"
                    raw_path.write_text(json.dumps(payload, ensure_ascii=True))

                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            INSERT INTO task_ai_score
                                (data_version, task_id, model, score, run_id, raw_json_ref, prompt_hash, input_hash)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (data_version, task_id, model, prompt_hash, input_hash) DO NOTHING
                            """,
                            (
                                data_version,
                                task_id,
                                model_label,
                                score,
                                run_id,
                                str(raw_path),
                                prompt_hash,
                                input_hash,
                            ),
                        )
                    conn.commit()

            except ProviderError as exc:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE model_run
                        SET status = %s,
                            error_message = %s,
                            error_at = NOW()
                        WHERE id = %s
                        """,
                        ("failed", str(exc), run_id),
                    )
                conn.commit()
                continue
            except Exception as exc:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE model_run
                        SET status = %s,
                            error_message = %s,
                            error_at = NOW()
                        WHERE id = %s
                        """,
                        ("failed", str(exc), run_id),
                    )
                conn.commit()
                continue
            else:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE model_run
                        SET status = %s
                        WHERE id = %s
                        """,
                        ("completed", run_id),
                    )
                conn.commit()

        task_ids = [task_id for task_id, _ in tasks]
        if task_ids:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO task_ai_ensemble (data_version, task_id, mean, std, min, max, updated_at)
                    SELECT
                        data_version,
                        task_id,
                        AVG(score)::numeric(6,2) AS mean,
                        STDDEV_POP(score)::numeric(6,2) AS std,
                        MIN(score)::numeric(6,2) AS min,
                        MAX(score)::numeric(6,2) AS max,
                        NOW()
                    FROM task_ai_score
                    WHERE data_version = %s
                      AND task_id = ANY(%s)
                    GROUP BY data_version, task_id
                    ON CONFLICT (data_version, task_id) DO UPDATE
                    SET mean = EXCLUDED.mean,
                        std = EXCLUDED.std,
                        min = EXCLUDED.min,
                        max = EXCLUDED.max,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (data_version, task_ids),
                )
            conn.commit()


if __name__ == "__main__":
    main()
