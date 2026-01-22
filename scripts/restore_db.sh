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

if ! command -v pg_restore >/dev/null 2>&1; then
  echo "pg_restore not found. Install libpq or PostgreSQL client tools." >&2
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

backup_dir="$ROOT_DIR/db/backups"
mapfile -t backups < <(ls -t "$backup_dir"/*.dump 2>/dev/null || true)

if [[ ${#backups[@]} -eq 0 ]]; then
  echo "No .dump backups found in $backup_dir" >&2
  exit 1
fi

auto_latest="${AUTO_LATEST_BACKUP:-1}"
if [[ "$auto_latest" == "1" ]]; then
  backup_file="${backups[0]}"
  echo "AUTO_LATEST_BACKUP=1 -> using latest backup:"
  echo "  $backup_file"
else
  echo "Select backup to restore:"
  for i in "${!backups[@]}"; do
    printf "  %d) %s\n" "$((i+1))" "${backups[$i]}"
  done

  echo -n "Enter number (default 1): "
  read -r selection

  if [[ -z "$selection" ]]; then
    selection=1
  fi

  if ! [[ "$selection" =~ ^[0-9]+$ ]]; then
    echo "Invalid selection: $selection" >&2
    exit 1
  fi

  index=$((selection-1))
  if [[ $index -lt 0 || $index -ge ${#backups[@]} ]]; then
    echo "Selection out of range" >&2
    exit 1
  fi

  backup_file="${backups[$index]}"
fi

echo "Restoring from: $backup_file"
pg_restore --clean --if-exists --no-owner --no-privileges -d "$DATABASE_URL" "$backup_file"

echo "Restore completed."
