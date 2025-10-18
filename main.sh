#!/bin/bash
set -e

echo "🧹 Limpando containers antigos..."
docker compose down -v --remove-orphans || true

echo "🐋 Buildando imagens..."
docker compose build

echo "🌐 Subindo servidores..."
docker compose up -d sequential_server concurrent_server

echo "⏳ Executando cliente de teste..."
docker compose run --rm client

echo ""
echo "✅ Testes concluídos. Resultados em resultados/resultados.csv"

# --- Abrir HTML automaticamente ---
if grep -qi microsoft /proc/version 2>/dev/null; then
  explorer.exe "$(wslpath -w "$(pwd)/index.html")"
elif command -v start >/dev/null; then
  start index.html
elif command -v xdg-open >/dev/null; then
  xdg-open index.html
elif command -v open >/dev/null; then
  open index.html
else
  echo "⚠️ Abra manualmente: $(pwd)/index.html"
fi
