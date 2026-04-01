#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

BACKUP_DIR="$1"
if [ -z "$BACKUP_DIR" ]; then
  echo "Uso: $0 <backup-dir>"
  exit 1
fi

mkdir -p "$BACKUP_DIR"
cp config/healthchecks.yml "$BACKUP_DIR/"
cp config/alerts.yml "$BACKUP_DIR/"
cp config/thresholds.yml "$BACKUP_DIR/"
cp database/init.sql "$BACKUP_DIR/"

echo "Backup de configuração criado em $BACKUP_DIR"

echo "Gerando dump de banco de dados MySQL..."
docker exec -i "$(docker ps -q -f "ancestor=mysql:8.0" | head -n 1)" mysqldump -uuser -ppass app > "$BACKUP_DIR/db_dump.sql" || true

echo "Backup concluído"
