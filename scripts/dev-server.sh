#!/usr/bin/env bash
# Stable Django dev server for local work.
# Run in a dedicated terminal (not via Cursor agent background shells).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON="${ROOT}/.venv/bin/python"
HOST="${DEV_HOST:-127.0.0.1}"
PORT="${DEV_PORT:-8000}"
RELOAD="${DEV_RELOAD:-0}"
WATCH="${DEV_WATCH:-1}"

if [[ ! -x "$PYTHON" ]]; then
  echo "Missing virtualenv at ${ROOT}/.venv — create it and install requirements first." >&2
  exit 1
fi

free_port() {
  if lsof -ti:"${PORT}" >/dev/null 2>&1; then
    echo "Stopping stale process on port ${PORT}..."
    lsof -ti:"${PORT}" | xargs kill -9 2>/dev/null || true
    sleep 1
  fi
}

run_server() {
  free_port
  local -a args=(manage.py rundev "${HOST}:${PORT}")
  if [[ "${RELOAD}" == "1" ]]; then
    args+=(--reload)
  fi
  echo "Dev server: http://${HOST}:${PORT}/ (Ctrl+C to stop)"
  "${PYTHON}" "${args[@]}"
}

trap 'echo "Dev server stopped."; exit 0' INT TERM

if [[ "${WATCH}" == "1" ]]; then
  while true; do
    run_server || {
      echo "Server exited at $(date). Restarting in 2s..."
      sleep 2
    }
  done
else
  run_server
fi
