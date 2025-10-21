# Trabalho de Redes II — Servidor Web Sequencial vs Concorrente

**Disciplina:** Redes de Computadores II  
**Curso:** Bacharelado em Sistemas de Informação — UFPI  
**Aluno:** Jorge Luis Ferreira Luz  
**Matrícula:** 20219040840

---

## Objetivo

Implementar dois servidores web (Sequencial e Concorrente) para comparar desempenho e comportamento entre abordagens síncrona e paralela. A comunicação segue o protocolo HTTP via sockets TCP, sem uso de frameworks como Flask, FastAPI ou Django.

---

## Estrutura do Projeto
```
Trabalho-Redes-2/
│
├── docker-compose.yml
├── Dockerfile
│
├── sequential_server.py      # Servidor Sequencial (porta 8080)
├── concurrent_server.py      # Servidor Concorrente (porta 8081)
├── client.py                 # Cliente automatizado de testes (métricas)
│
├── index.html                # Painel Web (UI para enviar requisições e medir latência)
└── resultados/               # Pasta gerada com resultados CSV
```

---

## Tecnologias Utilizadas

- **Python 3** (sockets, threading, hashlib)
- **HTTP via TCP puro**
- **Docker + Docker Compose** (simulação da rede)
- **HTML + JavaScript** (para o painel de testes)
- **SHA-1** (para gerar o cabeçalho criptográfico `X-Custom-ID`)

---

## Cabeçalho HTTP Personalizado (`X-Custom-ID`)

Cada requisição inclui um cabeçalho obrigatório calculado com:
```python
CUSTOM_ID = hashlib.sha1(f"{MATRICULA} {NOME}".encode()).hexdigest()
```

**Exemplo real:**
```python
MATRICULA = "20219040840"
NOME = "Jorge Luis Ferreira Luz"
X-Custom-ID: 8b33d991b6c4c6b80c1eec8ce2a03df00d39a4a4
```

O servidor valida a presença desse campo e retorna o mesmo valor no cabeçalho da resposta.

---

## Endereçamento da Rede Docker

A sub-rede foi configurada com base nos quatro últimos dígitos da matrícula (0840):
```
Sub-rede: 8.40.0.0/24
```

| Container    | IP        | Porta | Descrição              |
|--------------|-----------|-------|------------------------|
| client       | 8.40.0.2  | —     | Envia requisições e coleta métricas |
| seq_server   | 8.40.0.10 | 8080  | Servidor Sequencial    |
| conc_server  | 8.40.0.11 | 8081  | Servidor Concorrente   |

---

## Como Executar Tudo

### 1. Construir e iniciar os containers

No terminal, dentro da pasta do projeto:
```bash
docker compose up --build
```

Isso cria os três containers: `client`, `seq_server` e `conc_server`.

### 2. Executar o cliente de testes

Após os servidores iniciarem, entre no container do cliente:
```bash
docker exec -it client bash
```

E rode:
```bash
python3 client.py
```

O cliente enviará várias requisições `GET`, `POST`, `PUT`, `DELETE` para ambos os servidores, registrando:

- tempo médio (s)
- desvio padrão
- mínimo e máximo

Os resultados são salvos automaticamente em:
```
resultados/resultados.csv
```

### 3. Rodar o painel web (manual)

Abra o arquivo `index.html` manualmente no navegador.

> **Dica:** Se estiver usando VS Code, use "Go Live" ou "Live Server" para abrir em `http://127.0.0.1:5500/index.html`.

Esse painel envia requisições diretamente para:

- `http://localhost:8080` → servidor sequencial
- `http://localhost:8081` → servidor concorrente

e exibe:

- tempo médio por método
- desvio padrão
- logs e resposta HTTP completas (status, cabeçalhos, corpo)

> **Nota:** O `index.html` não é aberto automaticamente pelo script, deve ser aberto manualmente no navegador.

---

## Métricas Geradas

Cada execução gera uma linha no CSV com:
```csv
Servidor,Metodo,Media,DesvioPadrao,Min,Max,N
Sequencial,GET,0.001500,0.000210,0.001200,0.001700,30
Concorrente,POST,0.000800,0.000150,0.000600,0.001000,30
```

Esses valores são usados para:

- gerar gráficos de comparação
- calcular médias e desvios padrão
- identificar o cenário de melhor desempenho

---

## CORS e Validação

Os servidores incluem os cabeçalhos obrigatórios para permitir chamadas do navegador (`index.html`):
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, X-Custom-ID
Access-Control-Expose-Headers: X-Custom-ID, Content-Type, Content-Length
```

E validam o `X-Custom-ID`, respondendo `400 Bad Request` caso esteja ausente.

---

## Comandos Úteis

**Parar containers:**
```bash
docker compose down
```

**Ver logs:**
```bash
docker logs seq_server
docker logs conc_server
docker logs client
```

**Remover redes antigas:**
```bash
docker network prune -f
```

---

**Desenvolvido para a disciplina de Redes de Computadores II - UFPI**