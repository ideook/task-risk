import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from api.db import get_conn
from worker.llm_providers import (
    ProviderError,
    StructuredOutputSchema,
    env_flag,
    get_enabled_providers,
    get_provider,
    is_provider_enabled,
    parse_model_spec,
)
from worker.retry import retry_call

PROMPT_TEMPLATE = (
    "You are scoring AI impact for a single task. "
    "Return a JSON object that matches the provided schema exactly.\n"
    "Scoring rules:\n"
    "- ai_substitution_risk: 0-100, higher = easier to replace by AI.\n"
    "- ai_augmentation_potential: 0-100, higher = AI can strongly assist.\n"
    "- human_context_dependency: 0-100, higher = depends on human judgment/interaction.\n"
    "- physical_world_dependency: 0-100, higher = requires physical presence.\n"
    "- confidence: 0-1, higher = more confident.\n"
    "Use the AI Tech Progress context when present; if it says \"None\", treat as unknown.\n\n"
    "Task and context:\n{task_statement}"
)

SCORE_SCHEMA = StructuredOutputSchema(
    name="task_risk_scores",
    schema={
        "type": "object",
        "additionalProperties": False,
        "required": [
            "ai_substitution_risk",
            "ai_augmentation_potential",
            "human_context_dependency",
            "physical_world_dependency",
            "confidence",
        ],
        "properties": {
            "ai_substitution_risk": {"type": "number", "minimum": 0, "maximum": 100},
            "ai_augmentation_potential": {"type": "number", "minimum": 0, "maximum": 100},
            "human_context_dependency": {"type": "number", "minimum": 0, "maximum": 100},
            "physical_world_dependency": {"type": "number", "minimum": 0, "maximum": 100},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        },
    },
)


def hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def resolve_active_scope(
    conn, data_version: str, requested_week: Optional[str]
) -> Tuple[Optional[str], Optional[str]]:
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


def _ensure_json(value: Any) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        return json.loads(value)
    return dict(value)


def fetch_task_cards(
    conn, data_version: str, week: str, task_ids: List[int]
) -> Dict[int, Dict[str, Any]]:
    if not task_ids:
        return {}
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT DISTINCT ON (task_id) task_id, payload_json
            FROM tech_progress_llm_task_card
            WHERE data_version = %s
              AND week = %s
              AND task_id = ANY(%s)
            ORDER BY task_id, version DESC
            """,
            (data_version, week, task_ids),
        )
        rows = cur.fetchall()
    cards: Dict[int, Dict[str, Any]] = {}
    for task_id, payload in rows:
        parsed = _ensure_json(payload)
        if parsed is not None:
            cards[int(task_id)] = parsed
    return cards


def fetch_task_snapshots(
    conn, data_version: str, week: str, task_ids: List[int]
) -> Dict[int, Dict[str, Any]]:
    if not task_ids:
        return {}
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT task_id, progress_score, delta, top_changes_json
            FROM tech_progress_weekly_snapshot
            WHERE data_version = %s
              AND week = %s
              AND task_id = ANY(%s)
            """,
            (data_version, week, task_ids),
        )
        rows = cur.fetchall()
    snapshots: Dict[int, Dict[str, Any]] = {}
    for task_id, progress_score, delta, top_changes in rows:
        if isinstance(top_changes, str):
            try:
                top_changes = json.loads(top_changes)
            except json.JSONDecodeError:
                pass
        snapshots[int(task_id)] = {
            "progress_score": progress_score,
            "delta": delta,
            "top_changes_json": top_changes,
        }
    return snapshots


def _format_number(value: Any) -> str:
    if value is None:
        return "--"
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)


def format_progress_context(
    card: Optional[Dict[str, Any]],
    snapshot: Optional[Dict[str, Any]],
) -> str:
    if not card and not snapshot:
        return "None"
    source = card or snapshot or {}
    lines = [
        f"- progress_score: {_format_number(source.get('progress_score'))}",
        f"- delta: {_format_number(source.get('delta'))}",
    ]

    if card:
        changes = card.get("changes") or []
        if changes:
            lines.append("- changes:")
            for item in changes[:3]:
                tech = (
                    item.get("tech")
                    or item.get("tech_id")
                    or item.get("tech_name")
                    or "unknown"
                )
                link_type = item.get("link_type")
                impact = item.get("impact")
                evidence = item.get("evidence")
                detail = f"  - {tech}"
                if link_type:
                    detail += f" ({link_type})"
                if impact is not None:
                    detail += f" impact {_format_number(impact)}"
                if evidence:
                    detail += f" evidence {evidence}"
                lines.append(detail)
        evidence = card.get("evidence_briefs") or []
        if evidence:
            lines.append("- evidence:")
            for item in evidence[:3]:
                evidence_id = item.get("evidence_id") or "unknown"
                date = item.get("date") or ""
                summary = (item.get("summary") or "").strip().replace("\n", " ")
                detail = f"  - {evidence_id}"
                if date:
                    detail += f" ({date})"
                if summary:
                    detail += f": {summary}"
                lines.append(detail)
    else:
        changes = snapshot.get("top_changes_json") or []
        if changes:
            lines.append("- changes:")
            for change in changes[:3]:
                lines.append(f"  - {change}")

    return "\n".join(lines)


def build_task_input(task_statement: str, week: str, context: str) -> str:
    statement = (task_statement or "").strip()
    if not statement:
        statement = "Unknown task."
    context_value = (context or "").strip() or "None"
    lines = ["Task:", statement, ""]
    if week:
        lines.append(f"AI Tech Progress (week {week}):")
    else:
        lines.append("AI Tech Progress:")
    lines.append(context_value)
    return "\n".join(lines).strip()


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
    parser.add_argument(
        "--week",
        default=os.getenv("TECH_PROGRESS_WEEK"),
        help="Tech progress week (YYYY-Www). Defaults to latest active scope week.",
    )
    parser.add_argument("--max-retries", type=int, default=int(os.getenv("LLM_MAX_RETRIES", "3")))
    parser.add_argument("--retry-base-delay", type=float, default=float(os.getenv("LLM_RETRY_BASE_DELAY", "0.5")))
    parser.add_argument("--retry-max-delay", type=float, default=float(os.getenv("LLM_RETRY_MAX_DELAY", "10.0")))
    parser.add_argument("--retry-jitter", type=float, default=float(os.getenv("LLM_RETRY_JITTER", "0.2")))
    parser.add_argument("--verbose", action="store_true", default=env_flag("LLM_VERBOSE", "0"))
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
        week, active_id = resolve_active_scope(conn, data_version, args.week)
        if not week or not active_id:
            print(
                "[llm] no active scope",
                f"data_version={data_version}",
                f"week={args.week or 'latest'}",
                flush=True,
            )
            return

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT sat.task_id, ts.task_statement
                FROM tech_progress_scope_active_task sat
                JOIN task_statements ts
                  ON ts.data_version = sat.data_version
                 AND ts.task_id = sat.task_id
                LEFT JOIN task_catalog tc
                  ON tc.data_version = sat.data_version
                 AND tc.task_id = sat.task_id
                WHERE sat.active_id = %(active_id)s
                  AND sat.data_version = %(data_version)s
                ORDER BY tc.score DESC NULLS LAST, sat.task_id
                LIMIT %(limit)s
                """,
                {
                    "active_id": active_id,
                    "data_version": data_version,
                    "limit": args.limit,
                },
            )
            tasks = cur.fetchall()

        if not tasks:
            print(
                "[llm] no tasks",
                f"data_version={data_version}",
                f"week={week}",
                f"active_id={active_id}",
                flush=True,
            )
            return

        task_ids = [task_id for task_id, _ in tasks]
        task_cards = fetch_task_cards(conn, data_version, week, task_ids)
        task_snapshots = fetch_task_snapshots(conn, data_version, week, task_ids)

        if args.verbose:
            model_labels = [spec.label for spec in model_specs]
            print(
                "[llm] start",
                f"data_version={data_version}",
                f"week={week}",
                f"active_id={active_id}",
                f"tasks={len(tasks)}",
                f"models={model_labels}",
                f"mock={use_mock}",
                flush=True,
            )

        for spec in model_specs:
            model_label = spec.label
            if not is_provider_enabled(spec.provider, enabled_providers):
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO model_run (data_version, week, model, prompt_version, model_version, status, error_message)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            data_version,
                            week,
                            model_label,
                            args.prompt_version,
                            args.model_version,
                            "skipped",
                            f"Provider disabled: {spec.provider}",
                        ),
                    )
                conn.commit()
                if args.verbose:
                    print(
                        "[llm] skip",
                        f"model={model_label}",
                        f"reason=disabled({spec.provider})",
                        flush=True,
                    )
                continue

            try:
                provider = get_provider(spec, use_mock)
            except ProviderError as exc:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO model_run (data_version, week, model, prompt_version, model_version, status, error_message, error_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                        """,
                        (
                            data_version,
                            week,
                            model_label,
                            args.prompt_version,
                            args.model_version,
                            "failed",
                            str(exc),
                        ),
                    )
                conn.commit()
                if args.verbose:
                    print(
                        "[llm] fail",
                        f"model={model_label}",
                        f"error={exc}",
                        flush=True,
                    )
                continue
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO model_run (data_version, week, model, prompt_version, model_version, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        data_version,
                        week,
                        model_label,
                        args.prompt_version,
                        args.model_version,
                        "running",
                    ),
                )
                run_id = cur.fetchone()[0]
                conn.commit()

            prompt_hash = hash_text(
                f"{PROMPT_TEMPLATE}|{args.prompt_version}|{args.model_version}"
            )
            cache_hits = 0
            scored = 0
            if args.verbose:
                print("[llm] run", f"model={model_label}", f"run_id={run_id}", flush=True)
            try:
                for task_id, task_statement in tasks:
                    card = task_cards.get(task_id)
                    snapshot = task_snapshots.get(task_id)
                    context = format_progress_context(card, snapshot)
                    task_input = build_task_input(task_statement or "", week, context)
                    input_hash = hash_text(task_input)
                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            SELECT 1
                            FROM task_ai_score
                            WHERE data_version = %s
                              AND week = %s
                              AND task_id = %s AND model = %s
                              AND prompt_hash = %s AND input_hash = %s
                            """,
                            (
                                data_version,
                                week,
                                task_id,
                                model_label,
                                prompt_hash,
                                input_hash,
                            ),
                        )
                        if cur.fetchone():
                            cache_hits += 1
                            if args.verbose:
                                print(
                                    "[llm] cache",
                                    f"model={model_label}",
                                    f"task_id={task_id}",
                                    flush=True,
                                )
                            continue

                    def _score_call():
                        return provider.score(
                            task_input,
                            PROMPT_TEMPLATE,
                            args.prompt_version,
                            args.model_version,
                            schema=SCORE_SCHEMA,
                        )

                    scores = retry_call(
                        _score_call,
                        retries=args.max_retries,
                        base_delay=args.retry_base_delay,
                        max_delay=args.retry_max_delay,
                        jitter=args.retry_jitter,
                    )
                    scored += 1
                    substitution = scores.get("ai_substitution_risk")
                    if args.verbose:
                        print(
                            "[llm] score",
                            f"model={model_label}",
                            f"task_id={task_id}",
                            f"score={substitution}",
                            flush=True,
                        )
                    payload = {
                        "provider": spec.provider,
                        "model": spec.model,
                        "model_label": model_label,
                        "prompt_version": args.prompt_version,
                        "model_version": args.model_version,
                        "data_version": data_version,
                        "week": week,
                        "task_id": task_id,
                        "task_statement": task_statement,
                        "task_input": task_input,
                        "tech_progress_context": context,
                        "score": substitution,
                        "scores": scores,
                    }
                    safe_model = model_label.replace(":", "_").replace("/", "_")
                    safe_week = week.replace("/", "_")
                    raw_path = (
                        output_dir
                        / f"run_{run_id}_week_{safe_week}_task_{task_id}_{safe_model}.json"
                    )
                    raw_path.write_text(json.dumps(payload, ensure_ascii=True))

                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            INSERT INTO task_ai_score
                                (data_version, week, task_id, model, score, ai_substitution_risk,
                                 ai_augmentation_potential, human_context_dependency, physical_world_dependency,
                                 confidence, run_id, raw_json_ref, prompt_hash, input_hash)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (data_version, week, task_id, model, prompt_hash, input_hash) DO NOTHING
                            """,
                            (
                                data_version,
                                week,
                                task_id,
                                model_label,
                                substitution,
                                scores.get("ai_substitution_risk"),
                                scores.get("ai_augmentation_potential"),
                                scores.get("human_context_dependency"),
                                scores.get("physical_world_dependency"),
                                scores.get("confidence"),
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
                if args.verbose:
                    print(
                        "[llm] error",
                        f"model={model_label}",
                        f"error={exc}",
                        flush=True,
                    )
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
                if args.verbose:
                    print(
                        "[llm] error",
                        f"model={model_label}",
                        f"error={exc}",
                        flush=True,
                    )
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
                if args.verbose:
                    print(
                        "[llm] done",
                        f"model={model_label}",
                        f"scored={scored}",
                        f"cache_hits={cache_hits}",
                        flush=True,
                    )

        task_ids = [task_id for task_id, _ in tasks]
        if task_ids:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO task_ai_ensemble (
                        data_version, week, task_id,
                        mean, std, min, max,
                        ai_augmentation_potential_mean, ai_augmentation_potential_std,
                        ai_augmentation_potential_min, ai_augmentation_potential_max,
                        human_context_dependency_mean, human_context_dependency_std,
                        human_context_dependency_min, human_context_dependency_max,
                        physical_world_dependency_mean, physical_world_dependency_std,
                        physical_world_dependency_min, physical_world_dependency_max,
                        confidence_mean, confidence_std, confidence_min, confidence_max,
                        updated_at
                    )
                    SELECT
                        data_version,
                        week,
                        task_id,
                        AVG(score)::numeric(6,2) AS mean,
                        STDDEV_POP(score)::numeric(6,2) AS std,
                        MIN(score)::numeric(6,2) AS min,
                        MAX(score)::numeric(6,2) AS max,
                        AVG(ai_augmentation_potential)::numeric(6,2) AS ai_augmentation_potential_mean,
                        STDDEV_POP(ai_augmentation_potential)::numeric(6,2) AS ai_augmentation_potential_std,
                        MIN(ai_augmentation_potential)::numeric(6,2) AS ai_augmentation_potential_min,
                        MAX(ai_augmentation_potential)::numeric(6,2) AS ai_augmentation_potential_max,
                        AVG(human_context_dependency)::numeric(6,2) AS human_context_dependency_mean,
                        STDDEV_POP(human_context_dependency)::numeric(6,2) AS human_context_dependency_std,
                        MIN(human_context_dependency)::numeric(6,2) AS human_context_dependency_min,
                        MAX(human_context_dependency)::numeric(6,2) AS human_context_dependency_max,
                        AVG(physical_world_dependency)::numeric(6,2) AS physical_world_dependency_mean,
                        STDDEV_POP(physical_world_dependency)::numeric(6,2) AS physical_world_dependency_std,
                        MIN(physical_world_dependency)::numeric(6,2) AS physical_world_dependency_min,
                        MAX(physical_world_dependency)::numeric(6,2) AS physical_world_dependency_max,
                        AVG(confidence)::numeric(6,2) AS confidence_mean,
                        STDDEV_POP(confidence)::numeric(6,2) AS confidence_std,
                        MIN(confidence)::numeric(6,2) AS confidence_min,
                        MAX(confidence)::numeric(6,2) AS confidence_max,
                        NOW()
                    FROM task_ai_score
                    WHERE data_version = %s
                      AND week = %s
                      AND task_id = ANY(%s)
                    GROUP BY data_version, week, task_id
                    ON CONFLICT (data_version, week, task_id) DO UPDATE
                    SET mean = EXCLUDED.mean,
                        std = EXCLUDED.std,
                        min = EXCLUDED.min,
                        max = EXCLUDED.max,
                        ai_augmentation_potential_mean = EXCLUDED.ai_augmentation_potential_mean,
                        ai_augmentation_potential_std = EXCLUDED.ai_augmentation_potential_std,
                        ai_augmentation_potential_min = EXCLUDED.ai_augmentation_potential_min,
                        ai_augmentation_potential_max = EXCLUDED.ai_augmentation_potential_max,
                        human_context_dependency_mean = EXCLUDED.human_context_dependency_mean,
                        human_context_dependency_std = EXCLUDED.human_context_dependency_std,
                        human_context_dependency_min = EXCLUDED.human_context_dependency_min,
                        human_context_dependency_max = EXCLUDED.human_context_dependency_max,
                        physical_world_dependency_mean = EXCLUDED.physical_world_dependency_mean,
                        physical_world_dependency_std = EXCLUDED.physical_world_dependency_std,
                        physical_world_dependency_min = EXCLUDED.physical_world_dependency_min,
                        physical_world_dependency_max = EXCLUDED.physical_world_dependency_max,
                        confidence_mean = EXCLUDED.confidence_mean,
                        confidence_std = EXCLUDED.confidence_std,
                        confidence_min = EXCLUDED.confidence_min,
                        confidence_max = EXCLUDED.confidence_max,
                        updated_at = EXCLUDED.updated_at
                    """,
                    (data_version, week, task_ids),
                )
            conn.commit()


if __name__ == "__main__":
    main()
