#!/usr/bin/env bash
set -euo pipefail

echo "🧹 Limpando possíveis redes antigas (opcional)..."
docker network prune -f || true

echo "🧱 Buildando imagens..."
docker compose build

echo "🚀 Subindo servidores em background..."
docker compose up -d seq_server conc_server

echo "⏳ Aguardando 3s..."
sleep 3

echo "🧪 Executando cliente (testes + métricas)..."
docker compose run --rm client

echo "📈 Gerando gráfico..."
docker compose run --rm client python3 plot_results.py

echo "✅ Concluído. Veja arquivos em ./resultados/"
echo " - resultados.csv"
echo " - grafico_latency.png"

echo "🛑 (Opcional) Parar servidores: docker compose down"
chmod -R a+rw resultados || true
