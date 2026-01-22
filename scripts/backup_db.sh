#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_PATH="$ROOT_DIR/.env"

if [[ -f "$ENV_PATH" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ENV_PATH"
  set +a
fi

export PATH="/opt/homebrew/opt/libpq/bin:$PATH"

if ! command -v pg_dump >/dev/null 2>&1; then
  echo "pg_dump not found. Install libpq or PostgreSQL client tools." >&2
  exit 1
fi

if [[ -z "${DATABASE_URL:-}" ]]; then
  if [[ -z "${POSTGRES_DB:-}" || -z "${POSTGRES_USER:-}" || -z "${POSTGRES_PASSWORD:-}" ]]; then
    echo "DATABASE_URL or POSTGRES_* env vars must be set" >&2
    exit 1
  fi
  host="${POSTGRES_HOST:-localhost}"
  port="${POSTGRES_PORT:-5432}"
  DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${host}:${port}/${POSTGRES_DB}"
fi

db_name="${POSTGRES_DB:-task_risk}"
backup_dir="$ROOT_DIR/db/backups"
mkdir -p "$backup_dir"

ts="$(date +%Y%m%d_%H%M%S)"
backup_file="$backup_dir/${db_name}_full_${ts}.dump"

pg_dump "$DATABASE_URL" -F c -b -v --no-owner --no-privileges -f "$backup_file"

echo "Backup created: $backup_file"
