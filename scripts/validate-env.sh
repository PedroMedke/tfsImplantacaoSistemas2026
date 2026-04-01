#!/bin/bash
set -e

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker não encontrado. Instale Docker antes de prosseguir."
  exit 1
fi

if ! command -v docker-compose >/dev/null 2>&1; then
  echo "Docker Compose não encontrado. Instale Docker Compose antes de prosseguir."
  exit 1
fi

echo "Ambiente validado."
