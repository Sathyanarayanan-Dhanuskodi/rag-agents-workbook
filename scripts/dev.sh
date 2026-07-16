#!/usr/bin/env bash
# The one command: bootstrap if needed, then run backend + frontend together.
# Ctrl+C stops both.
set -euo pipefail
cd "$(dirname "$0")/.."

bash scripts/setup.sh

printf '\n  \033[36mbackend \033[0m http://localhost:8000  (API docs at /docs)\n'
printf '  \033[35mfrontend\033[0m http://localhost:3000\n\n'

# The backend runs with cwd=backend on purpose: config.py resolves .env,
# ./chroma_db and ./data relative to the working directory.
exec pnpm exec concurrently \
  --names "backend,frontend" \
  --prefix-colors "cyan.bold,magenta.bold" \
  --kill-others \
  "cd backend && .venv/bin/uvicorn app.main:app --reload --port 8000" \
  "pnpm --filter rag-frontend dev"
