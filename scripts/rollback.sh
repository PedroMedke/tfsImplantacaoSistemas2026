#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

BACKUP_DIR="$1"

if [ -z "$BACKUP_DIR" ]; then
  echo "Uso: $0 <backup-dir>"
  exit 1
fi

if [ ! -d "$BACKUP_DIR" ]; then
  echo "Backup não encontrado: $BACKUP_DIR"
  exit 1
fi

echo "Rollback iniciado usando backup em $BACKUP_DIR"

if [ -f "$BACKUP_DIR/healthchecks.yml" ]; then
  cp "$BACKUP_DIR/healthchecks.yml" config/healthchecks.yml
fi

if [ -f "$BACKUP_DIR/alerts.yml" ]; then
  cp "$BACKUP_DIR/alerts.yml" config/alerts.yml
fi

if [ -f "$BACKUP_DIR/init.sql" ]; then
  echo "Restaurando dump de banco de dados..."
  docker exec -i "$(docker ps -q -f "ancestor=mysql:8.0" | head -n 1)" mysql -uuser -ppass app < "$BACKUP_DIR/init.sql" || true
fi

echo "Rollback concluído"
