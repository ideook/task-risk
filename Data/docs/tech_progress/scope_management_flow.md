# Active Scope Management Flow

## Roles and permissions
- Admin: manage defined scopes, create/activate/archieve active scopes, edit evidence
- Analyst: create drafts, edit items, request activation
- Reviewer: approve activation, archive
- Viewer: read-only

## State model for active scope
- draft -> active -> archived
- Only one active scope per week

## Flow: create active scope
1) Select defined scope
2) Choose week
3) Draft created (status=draft)
4) Add/remove items (occupation/task)
5) Preview expanded tasks
6) Activate (if no other active scope for week)

## Flow: change active scope
1) Duplicate active scope into new draft
2) Edit items
3) Preview tasks
4) Activate new draft (auto-archive previous active)

## Guardrails
- If scope_type=occupation, auto-expand tasks from occupation
- If scope_type=task, only listed tasks are included
- Prevent activation if expanded task list is empty
- Log every change event

## Audit log events
- scope_defined.created
- scope_defined.updated
- scope_active.created
- scope_active.item_added
- scope_active.item_removed
- scope_active.previewed
- scope_active.activated
- scope_active.archived

## UI checklist
- Show active scope per week
- Show preview counts before activation
- Show change diff vs previous week
- Show who activated and when
