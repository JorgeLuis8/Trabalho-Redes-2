#!/bin/bash
set -e

echo "🧹 Limpando containers..."
docker compose down -v --remove-orphans || true
docker network prune -f || true

echo "📁 Garantindo pasta de resultados..."
mkdir -p resultados

echo "🐋 Buildando imagens..."
docker compose build

echo "🌐 Subindo servidores..."
docker compose up -d sequential_server concurrent_server

echo "🧪 Executando cliente de testes (30x por método)..."
docker compose run --rm client

echo ""
echo "✅ Concluído!"
echo "📊 CSV: $(pwd)/resultados/resultados.csv"
echo "ℹ️ No terminal acima você tem as AMOSTRAS de respostas HTTP (headers + body) para cada método e servidor."
