#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "Iniciando deploy..."

./scripts/backup.sh "$BACKUP_DIR"

echo "Executando healthcheck pré-deploy..."
./scripts/health-monitor.sh --pre-deploy

echo "Subindo novos serviços com zero downtime..."
docker-compose up -d --build api dashboard
sleep 15

if ./scripts/health-monitor.sh --check-all; then
    echo "Novo serviço saudável, deploy concluído com sucesso!"
else
    echo "Falha no deploy, executando rollback..."
    ./scripts/rollback.sh "$BACKUP_DIR"
    exit 1
fi
