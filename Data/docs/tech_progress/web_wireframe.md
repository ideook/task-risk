# Web Wireframes (Text)

## 1) Active Scope Manager
```
[Header]  Scope Manager  | Week: 2026-W03 | Status: Draft/Active

[Left] Defined Scopes
- Support and Ops (SCOPE-DEF-001)
- ...

[Center] Active Scope Builder
Selected Scope: Support and Ops
Week: 2026-W03

[Tabs] Occupations | Tasks | Summary

Occupations (from defined)
[ ] OCC-001 Customer Support Analyst
[ ] OCC-002 Operations Scheduler

[Actions]
- Apply selection -> generate active scope
- Save draft
- Activate scope

[Right] Preview: Expanded Tasks
T1001 Categorize incoming support tickets...
T1002 Draft responses to common inquiries...
T2001 Create weekly staff schedules...
T2002 Monitor SLA compliance...
```

## 2) Weekly Dashboard
```
[Header] Weekly Tech Progress | Week: 2026-W03 | Scope: Active

[Top KPIs]
- Tasks with change: 12
- Avg progress score: 0.54
- Top tech domains: NLP, Ops

[Section] Top Changing Tasks
- T1002 +0.12  (LLM Assistant)
- T1001 +0.10  (LLM Assistant)

[Section] Tech Trend Cards
- TECH-LLM-001: impacts 7 tasks, avg impact 0.61
- TECH-WFM-001: impacts 4 tasks, avg impact 0.52

[Filters]
- Task category | Link type | Confidence | Evidence quality
```

## 3) Task Detail
```
[Header] Task T1001 | Week: 2026-W03

[Left] Task Info
- Text
- Category
- Occupation
- Progress score & delta

[Center] Linked Technologies
- TECH-LLM-001 (automates, impact 0.64, conf 0.70)
- ...

[Right] Evidence
- E2026W03-002 (paper) summary...

[Bottom] History
Week 2026-W02 -> 2026-W03 -> 2026-W04
```

## 4) Technology Detail
```
[Header] TECH-LLM-001

[Left] Tech Info
- Name, domain, synonyms

[Center] Impacted Tasks (top)
- T1002 (augments, 0.72)
- T1001 (automates, 0.64)

[Right] Evidence timeline
- E2026W03-001
- E2026W03-002
```

## 5) Evidence Library
```
[Header] Evidence Library

[Filters]
- Source type | Date range | Quality score

[List]
- E2026W03-001 | product_release | 0.78 | summary...
- E2026W03-002 | paper | 0.82 | summary...
```

## 6) Week Compare
```
[Header] Compare Weeks
Week A: 2026-W02   Week B: 2026-W03

[Delta Table]
Task | A score | B score | Delta | Main change
T1001 | 0.48 | 0.58 | +0.10 | TECH-LLM-001 automates
```
