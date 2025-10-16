# 🧪 Projeto — Servidores Web Sequencial e Concorrente

**Disciplina:** Redes de Computadores II — UFPI  
**Autor:** Jorge Luis Ferreira Luz — Matrícula 20219040840

---

## 🎯 Objetivo

Implementar e comparar o desempenho entre um **servidor web sequencial** e um **concorrente** utilizando **Python + Sockets (TCP)** e **mensagens HTTP**.

---

## 🧩 Estrutura do Projeto
```
Trabalho-Redes-2/
├── sequential_server.py
├── concurrent_server.py
├── test_metrics.py
├── docker-compose.yml
├── run_all.sh
└── resultados/
    └── resultados.csv
```

---

## 🐳 Execução Automática

### 1️⃣ Dê permissão ao script:
```bash
chmod +x run_all.sh
```

### 2️⃣ Execute todos os testes:
```bash
./run_all.sh
```

### O script realiza:

- ✅ Limpeza de containers antigos
- ✅ Build e inicialização dos servidores
- ✅ Execução do cliente de teste
- ✅ Salvamento das métricas de latência em `resultados/resultados.csv`

---

## 📈 Métricas Coletadas

| Métrica | Descrição |
|---------|-----------|
| **Média** | Tempo médio de resposta por método |
| **Desvio Padrão** | Variação do tempo médio |
| **Latência Mínima** | Menor tempo observado |
| **Latência Máxima** | Maior tempo observado |

---

## 🧮 Formato dos Resultados

O arquivo `resultados/resultados.csv` contém as seguintes colunas:
```csv
Servidor,Metodo,Media,Desvio,Min,Max
Sequencial,GET,0.00023,0.00004,0.00019,0.00030
Concorrente,GET,0.00112,0.00058,0.00046,0.00281
...
```

---

## 🌐 Acesso Manual aos Servidores

| Servidor | URL |
|----------|-----|
| **Sequencial** | http://localhost:8080 |
| **Concorrente** | http://localhost:8081 |

---

## 🧾 Observações

- 📁 Todos os resultados são salvos em: `resultados/`
- 🔄 O script gerencia automaticamente o ciclo completo de teste
- 📊 Os dados são persistidos para análise posterior

---

## 🚀 Execução Rápida
```bash
./run_all.sh
```

**Resultado esperado:**  
Arquivo gerado em `Trabalho-Redes-2/resultados/resultados.csv` com todas as métricas coletadas.

---