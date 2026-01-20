# LLM Payload Format (Mock)

## Recommended delivery method
- Primary: query tables and build payloads from `llm_task_card` and `llm_weekly_summary`.
- Optional: materialized view or week-level JSON export for caching.

Why tables first:
- deterministic, versionable, reproducible
- easy to filter by active scope and week
- low token footprint via pre-assembled cards

## Task Card (llm_task_card.payload_json)
```json
{
  "week": "2026-W03",
  "task_id": "T1001",
  "task_text": "...",
  "progress_score": 0.58,
  "delta": 0.10,
  "changes": [
    {"tech": "TECH-LLM-001", "link_type": "automates", "impact": 0.64, "evidence": "E2026W03-002"}
  ],
  "evidence_briefs": [
    {"evidence_id": "E2026W03-002", "summary": "...", "date": "2026-01-15"}
  ]
}
```

Field rules
- `week`: YYYY-Www
- `progress_score`: 0.00-1.00
- `delta`: -1.00-1.00 (weekly change)
- `changes`: ordered by impact desc
- `evidence_briefs`: only top 1-3 per task

Size guidance
- Prefer <= 800-1200 chars per card
- Truncate summaries to 160-240 chars
- Keep `changes` <= 3 per task

## Weekly Summary (llm_weekly_summary.payload_json)
```json
{
  "week": "2026-W03",
  "top_tasks": [
    {"task_id": "T1002", "delta": 0.12},
    {"task_id": "T1001", "delta": 0.10}
  ],
  "notes": [
    "Short bullet summary of week-level shifts."
  ]
}
```

## Selection logic (LLM input)
- Filter by `scope_active_task` for the target week.
- Include only tasks with `delta != 0` by default; allow override.
- Provide 2-4 week window when trend analysis is requested.

## Alternatives (if table delivery is not ideal)
- Materialized view per week: faster reads, less app logic
- Week-level JSON export: easy to stream to LLM, but harder to update incrementally
- Vector store: useful for semantic search, but keep as secondary index (do not replace tables)
