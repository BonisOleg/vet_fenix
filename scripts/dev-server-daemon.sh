#!/usr/bin/env bash
# Start/stop Django dev server detached from the terminal (survives IDE sessions).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PID_FILE="${ROOT}/.dev-server.pid"
LOG_FILE="${ROOT}/.dev-server.log"
HOST="${DEV_HOST:-127.0.0.1}"
PORT="${DEV_PORT:-8000}"

is_running() {
  [[ -f "$PID_FILE" ]] || return 1
  local pid
  pid="$(cat "$PID_FILE")"
  kill -0 "$pid" 2>/dev/null
}

cmd_start() {
  if is_running; then
    echo "Dev server already running (PID $(cat "$PID_FILE"))."
    echo "http://${HOST}:${PORT}/"
    exit 0
  fi
  : >"$LOG_FILE"
  DEV_WATCH=1 nohup "${ROOT}/scripts/dev-server.sh" >>"$LOG_FILE" 2>&1 &
  echo $! >"$PID_FILE"
  sleep 2
  if ! is_running; then
    echo "Failed to start. Last log lines:" >&2
    tail -20 "$LOG_FILE" >&2 || true
    rm -f "$PID_FILE"
    exit 1
  fi
  echo "Dev server started (PID $(cat "$PID_FILE"))."
  echo "http://${HOST}:${PORT}/"
  echo "Log: ${LOG_FILE}"
}

cmd_stop() {
  if ! is_running; then
    rm -f "$PID_FILE"
    lsof -ti:"${PORT}" 2>/dev/null | xargs kill -9 2>/dev/null || true
    echo "Dev server was not running."
    exit 0
  fi
  local pid
  pid="$(cat "$PID_FILE")"
  kill "$pid" 2>/dev/null || true
  sleep 1
  kill -9 "$pid" 2>/dev/null || true
  lsof -ti:"${PORT}" 2>/dev/null | xargs kill -9 2>/dev/null || true
  rm -f "$PID_FILE"
  echo "Dev server stopped."
}

cmd_status() {
  if is_running; then
    echo "Running (PID $(cat "$PID_FILE")) — http://${HOST}:${PORT}/"
    curl -s -o /dev/null -w "HTTP %{http_code}\n" "http://${HOST}:${PORT}/" 2>/dev/null || true
  else
    echo "Not running."
    exit 1
  fi
}

case "${1:-}" in
  start) cmd_start ;;
  stop) cmd_stop ;;
  status) cmd_status ;;
  restart) cmd_stop; cmd_start ;;
  *)
    echo "Usage: $0 {start|stop|status|restart}" >&2
    exit 1
    ;;
esac
