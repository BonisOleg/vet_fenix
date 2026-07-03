#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)

echo "==> Звільнення портів 80/443 на хості..."
systemctl stop nginx gunicorn-* 2>/dev/null || true

echo "==> Збірка образів..."
"${COMPOSE[@]}" build --no-cache

echo "==> Запуск контейнерів..."
"${COMPOSE[@]}" up -d

echo "==> Міграції..."
"${COMPOSE[@]}" exec -T backend python manage.py migrate --noinput

echo "==> Перевірка healthcheck..."
if curl -sf http://127.0.0.1/healthz/ >/dev/null; then
  echo "==> Deploy done. HTTP OK: http://127.0.0.1/healthz/"
else
  echo "WARN: /healthz/ не відповів — перевір: ${COMPOSE[*]} logs backend nginx"
  exit 1
fi
