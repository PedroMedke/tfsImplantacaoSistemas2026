#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Executando limpeza de recursos antigos..."

docker container prune -f
docker image prune -f

echo "Removendo backups com mais de 30 dias..."
find "$ROOT_DIR/backups" -maxdepth 1 -type d -mtime +30 -print -exec rm -rf {} + 2>/dev/null || true

if [ -d "/var/log" ]; then
  echo "Limpando logs antigos de sistema..."
  find /var/log -type f -name '*.log' -mtime +30 -delete 2>/dev/null || true
fi

echo "Limpeza concluída"
