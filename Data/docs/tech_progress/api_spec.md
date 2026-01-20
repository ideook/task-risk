# API Spec (Mock)

Base: /api/v1

## Scope management

GET /scopes/defined
- Query: status, type
- Response: list of defined scopes

POST /scopes/defined
- Body: { name, scope_type, description }
- Response: scope_id

PATCH /scopes/defined/{scope_id}
- Body: { name?, status?, description? }

POST /scopes/defined/{scope_id}/items
- Body: { item_type, item_id }

DELETE /scopes/defined/{scope_id}/items
- Body: { item_type, item_id }

GET /scopes/active
- Query: week, status

POST /scopes/active
- Body: { week, scope_id, created_by }
- Creates draft active scope

POST /scopes/active/{active_id}/items
- Body: { item_type, item_id }

POST /scopes/active/{active_id}/preview
- Response: expanded task list (derived from selected occupation/task)

POST /scopes/active/{active_id}/activate
- Rule: only one active scope per week

POST /scopes/active/{active_id}/archive

## Tasks and tech

GET /tasks
- Query: week, scope=active, category, occupation, delta_min, delta_max

GET /tasks/{task_id}
- Query: week

GET /tasks/{task_id}/history
- Query: weeks=4

GET /technologies
- Query: domain, status

GET /technologies/{tech_id}

GET /technologies/{tech_id}/impact
- Query: week, scope=active

## Evidence

GET /evidence
- Query: source_type, date_from, date_to, quality_min

POST /evidence
- Body: { source_id, evidence_date, summary, quality_score, raw_ref }

## Links and snapshots

POST /links
- Body: { week, task_id, tech_id, link_type, impact_score, confidence, evidence_id }

GET /snapshots
- Query: week, scope=active

## LLM payload

GET /llm/weekly
- Query: week, scope=active, version=latest

GET /llm/tasks
- Query: week, scope=active, delta_only=true

## Example: Task detail response
```json
{
  "task_id": "T1001",
  "task_text": "Categorize incoming support tickets by issue type.",
  "week": "2026-W03",
  "progress_score": 0.58,
  "delta": 0.18,
  "links": [
    {
      "tech_id": "TECH-LLM-001",
      "link_type": "automates",
      "impact_score": 0.64,
      "confidence": 0.70,
      "evidence_id": "E2026W03-002"
    }
  ],
  "evidence": [
    {
      "evidence_id": "E2026W03-002",
      "summary": "Automatic ticket triage reduces handling time with minimal error.",
      "date": "2026-01-15"
    }
  ]
}
```
