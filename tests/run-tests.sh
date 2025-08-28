#!/usr/bin/env bash
set -euo pipefail

# Wait for PostgreSQL to be ready
until pg_isready -h db -p 5432 -U "$POSTGRES_USER" >/dev/null 2>&1; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Prepare clean test database
export PGPASSWORD="$POSTGRES_PASSWORD"
psql -h db -U "$POSTGRES_USER" -d postgres -c "DROP DATABASE IF EXISTS test_app;"
psql -h db -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE test_app;"

# Run migrations
alembic -x sqlalchemy.url="$TEST_DATABASE_URL" upgrade head

# Execute tests
pytest "$@"
