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

if [[ -z "${DATABASE_URL:-}" ]]; then
  if [[ -z "${POSTGRES_DB:-}" || -z "${POSTGRES_USER:-}" || -z "${POSTGRES_PASSWORD:-}" ]]; then
    echo "DATABASE_URL or POSTGRES_* env vars must be set" >&2
    exit 1
  fi
  host="${POSTGRES_HOST:-localhost}"
  port="${POSTGRES_PORT:-5432}"
  DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${host}:${port}/${POSTGRES_DB}"
fi

psql "${DATABASE_URL}" -f "$ROOT_DIR/db/schema.sql"
