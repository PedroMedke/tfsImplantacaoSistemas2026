#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Iniciando build automatizado..."

./scripts/validate-env.sh

echo "Construindo imagens de containers..."
docker-compose build --no-cache

./scripts/validate-images.sh

echo "Build concluído com sucesso!"
