#!/usr/bin/env bash
# Start the FastAPI backend with hot-reload on http://localhost:8000
#
# Prefer `pnpm dev` from the repo root — it starts the frontend too.
# This script runs the backend alone; it uses ../backend/.venv when present,
# so you don't have to activate it first.
set -e
cd "$(dirname "$0")"

if [ -x .venv/bin/uvicorn ]; then
  exec .venv/bin/uvicorn app.main:app --reload --port 8000
fi

exec uvicorn app.main:app --reload --port 8000
