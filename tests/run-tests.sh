#!/usr/bin/env bash
set -euo pipefail

# Simple readiness wait for PostgreSQL with timeout
HOST="${POSTGRES_HOST:-localhost}"
PORT="${POSTGRES_PORT:-5432}"
SLEEP_INTERVAL=1
MAX_WAIT="${POSTGRES_READY_TIMEOUT:-30}"

elapsed=0
while ! nc -z "$HOST" "$PORT" >/dev/null 2>&1; do
  if [ "$elapsed" -ge "$MAX_WAIT" ]; then
    echo "ERROR: PostgreSQL is still unreachable at ${HOST}:${PORT} after ${MAX_WAIT}s." >&2
    exit 1
  fi
  echo "Waiting for PostgreSQL at ${HOST}:${PORT}... (${elapsed}s elapsed)"
  sleep "$SLEEP_INTERVAL"
  elapsed=$((elapsed + SLEEP_INTERVAL))
done

echo "PostgreSQL is up after ${elapsed}s. Running tests..."
pytest "$@"
