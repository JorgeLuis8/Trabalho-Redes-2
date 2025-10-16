#!/bin/bash
set -e

echo "====================================="
echo "Redes de Computadores II - Execução Completa"
echo "====================================="

# Cria pasta de resultados
mkdir -p resultados

# Etapa 1: Build
echo "Buildando containers..."
docker compose --env-file .env build

# Etapa 2: Servidor SEQUENCIAL
echo "Subindo servidor SEQUENCIAL e cliente..."
docker compose up -d servidor_sequencial cliente

echo "Aguardando inicialização..."
sleep 4

echo "Executando experimentos SEQUENCIAIS..."
docker exec cliente python3 executar_experimentos.py || true

echo "Removendo containers SEQUENCIAIS..."
docker compose down

# Etapa 3: Servidor CONCORRENTE
echo "Subindo servidor CONCORRENTE e cliente..."
docker compose up -d servidor_concorrente cliente

echo "Aguardando inicialização..."
sleep 4

echo "Executando experimentos CONCORRENTES..."
docker exec cliente python3 executar_experimentos.py || true

echo "Removendo containers CONCORRENTES..."
docker compose down

# Etapa 4: Geração de gráficos
CSV_FILE=$(ls resultados/metricas_*.csv | sort | tail -n 1)

if [ -f "$CSV_FILE" ]; then
    echo "Gerando gráficos e estatísticas..."
    docker exec cliente python3 plot_metricas.py "$CSV_FILE" || true
else
    echo "Nenhum arquivo CSV encontrado para gerar gráficos."
fi

# Conclusão
echo "====================================="
echo "Execução concluída com sucesso."
echo "Resultados disponíveis em ./resultados/"
echo "====================================="
