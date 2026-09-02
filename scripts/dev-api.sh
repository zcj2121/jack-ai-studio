#!/bin/sh

set -eu

api_env_file="apps/api/.env"

if [ -f "$api_env_file" ]; then
  exec uv run --env-file "$api_env_file" uvicorn app.main:app \
    --app-dir apps/api --host 127.0.0.1 --port 8000
fi

exec uv run uvicorn app.main:app \
  --app-dir apps/api --host 127.0.0.1 --port 8000
