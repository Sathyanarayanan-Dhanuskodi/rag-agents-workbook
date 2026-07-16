#!/usr/bin/env bash
# Idempotent bootstrap: venv + python deps + node deps + .env files.
# Safe to re-run; each step is skipped when it's already done.
# Called automatically by `pnpm dev`, or run on its own with `pnpm setup`.
set -euo pipefail
cd "$(dirname "$0")/.."

say() { printf '\033[36m[setup]\033[0m %s\n' "$1"; }
warn() { printf '\033[33m[setup]\033[0m %s\n' "$1"; }

# --- 1. Python venv ---------------------------------------------------------
if [ ! -x backend/.venv/bin/python ]; then
  say "creating backend/.venv"
  python3 -m venv backend/.venv
fi

# --- 2. Python deps (re-installed only when requirements.txt changes) -------
stamp=backend/.venv/.requirements-sha
want=$(sha256sum backend/requirements.txt | cut -d' ' -f1)
if [ "$(cat "$stamp" 2>/dev/null || true)" != "$want" ]; then
  say "installing python deps (first run takes a few minutes)"
  backend/.venv/bin/pip install --quiet --upgrade pip
  backend/.venv/bin/pip install --quiet -r backend/requirements.txt
  echo "$want" > "$stamp"
fi

# --- 3. Node deps (pnpm workspace: root + frontend) -------------------------
if ! command -v pnpm >/dev/null 2>&1; then
  warn "pnpm not found — install it with: npm install -g pnpm    (https://pnpm.io/installation)"
  exit 1
fi
if [ ! -d node_modules ] || [ ! -d frontend/node_modules ]; then
  say "installing node deps"
  pnpm install --silent
fi

# --- 4. .env files ----------------------------------------------------------
[ -f backend/.env ] || { say "creating backend/.env"; cp backend/.env.example backend/.env; }
[ -f frontend/.env.local ] || { say "creating frontend/.env.local"; cp frontend/.env.local.example frontend/.env.local; }

# --- 5. Ollama preflight (warn only — the app still starts without it) ------
if ! curl -sf -m 2 http://localhost:11434/api/tags >/dev/null 2>&1; then
  warn "Ollama isn't responding on :11434 — ingest/query will fail until you start it."
  warn "  https://ollama.com/download"
else
  tags=$(curl -sf -m 2 http://localhost:11434/api/tags || true)
  for model in llama3.2 nomic-embed-text; do
    case "$tags" in
      *"\"$model"*) ;;
      *) warn "model '$model' not pulled yet — run: ollama pull $model" ;;
    esac
  done
fi
