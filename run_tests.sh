#!/bin/bash
set -e

echo ""
echo "🧹 Limpando containers e redes antigas..."
docker compose down -v
docker network prune -f

echo ""
echo "🚀 Buildando containers..."
docker compose build

echo ""
echo "🌐 Subindo servidores em segundo plano..."
docker compose up -d sequential_server concurrent_server

echo ""
echo "📡 Executando cliente de testes..."
docker compose run --rm client

echo ""
echo "✅ Testes concluídos! Resultados salvos em resultados.csv"
echo "🗂️ Local: $(pwd)/resultados.csv"
