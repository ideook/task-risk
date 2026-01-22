# DB Backup Notes

## Formats
- `*.sql` (plain text): human-readable SQL dump. Restore with `psql -f`.
- `*.dump` (custom format): binary/custom pg_dump format. Restore with `pg_restore`.

## Current standard
- Use **custom format** backups: `db/backups/task_risk_full_YYYYMMDD_HHMMSS.dump`
- 이유: 빠른 복원, 특정 테이블 선택 복원 가능, 용량 효율

## Scripts
- Backup: `scripts/backup_db.sh`
- Restore: `scripts/restore_db.sh`

## Restore behavior
- Restore script **overwrites** the target DB (drops existing objects and restores).
