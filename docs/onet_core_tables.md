# O*NET Core Tables (task-risk)

Purpose: document the minimal O*NET tables/columns used by this project.
Source: O*NET 30.1 MySQL dump in `Data/db_30_1_mysql`.

Notes
- All O*NET-derived tables in this project are versioned by `data_version`.
- `scale_id='IM'` (importance) is used for task catalog/weights by default.

1) Occupation data
- Source file: `03_occupation_data.sql`
- Raw columns used: `onetsoc_code`, `title`, `description`
- Project table: `occupation_master`
  - `data_version`, `onetsoc_code`, `soc_code`, `title`, `description`

2) Alternate titles
- Source file: `29_alternate_titles.sql`
- Raw columns used: `onetsoc_code`, `alternate_title`, `short_title`
- Project table: `alternate_titles`
  - `data_version`, `onetsoc_code`, `alternate_title`, `short_title`

3) Task statements
- Source file: `17_task_statements.sql`
- Raw columns used: `task_id`, `task`
- Project table: `task_statements`
  - `data_version`, `task_id`, `task_statement`

4) Task ratings
- Source file: `18_task_ratings.sql`
- Raw columns used:
  - `onetsoc_code`, `task_id`, `scale_id`, `category`, `data_value`,
    `n`, `standard_error`, `lower_ci_bound`, `upper_ci_bound`,
    `recommend_suppress`, `date_updated`, `domain_source`
- Project table: `occupation_task_ratings`
  - Same columns + `data_version`

Derived tables (project generated)
- `task_catalog`: top N tasks by average `data_value` for `scale_id`.
- `occupation_task_weight`: normalized weights per `soc_code` (sum=1).
- `task_ai_score`, `task_ai_ensemble`, `occupation_ai_score`: AI scoring outputs.

Data versioning
- `data_version` table stores all known O*NET versions and an optional active flag.
- `batch/set_active_version.py` sets the active version for API defaults.
