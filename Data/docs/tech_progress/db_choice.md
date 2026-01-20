# Database choice and assumptions

Primary target: PostgreSQL 15+
- jsonb support and indexing for payloads and change lists
- partial index for a single active scope per week
- materialized views if needed for weekly payloads

Secondary target: MySQL 8.0.16+
- supported as a compatibility variant (see schema_mysql.sql)
- no partial index, enforce single-active-scope rule at app layer

If a different database is required, update the schema files before implementation.
