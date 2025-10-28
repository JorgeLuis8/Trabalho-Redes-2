# Segunda Avaliação — Redes de Computadores II (2025.2)

**Disciplina:** Redes de Computadores II  
**Curso:** Bacharelado em Sistemas de Informação — UFPI  
**Aluno:** Jorge Luis Ferreira Luz  
**Matrícula:** 20219040840

---

##  Vídeo de Explicação

**Link do YouTube:** [Clique aqui para assistir](URL_DO_VIDEO_AQUI)

> Vídeo demonstrando a execução do projeto, funcionamento dos servidores e análise dos resultados obtidos.

---

## Objetivo

Implementar dois servidores web — **Sequencial** e **Concorrente** — para comparar desempenho e comportamento entre abordagens síncrona e paralela.

A comunicação é feita por HTTP sobre TCP, usando sockets puros, sem bibliotecas de alto nível (como Flask, FastAPI ou Django).

---

## Estrutura do Projeto
```
Trabalho-Redes-2/
│
├── main.sh                   # Script principal que monta tudo automaticamente
├── docker-compose.yml
├── Dockerfile
│
├── sequential_server.py       # Servidor Sequencial (porta 8080)
├── concurrent_server.py       # Servidor Concorrente (porta 8081)
├── client.py                  # Cliente automatizado de testes (gera CSV)
│
└── resultados/                # Pasta onde o CSV é salvo automaticamente
```

---

## Tecnologias Utilizadas

- **Python 3** — sockets, threading, hashlib
- **HTTP via TCP** — estrutura manual de requisições e respostas
- **Docker + Docker Compose** — isolamento e rede simulada
- **Bash Script (main.sh)** — automação da execução
- **SHA-1** — geração do cabeçalho criptográfico X-Custom-ID

---

## Cabeçalho HTTP Personalizado (X-Custom-ID)

Cada requisição enviada pelo cliente inclui o cabeçalho obrigatório calculado como:
```python
CUSTOM_ID = hashlib.sha1(f"{MATRICULA} {NOME}".encode()).hexdigest()
```

**Exemplo real:**
```python
MATRICULA = "20219040840"
NOME = "Jorge Luis Ferreira Luz"

X-Custom-ID: 8b33d991b6c4c6b80c1eec8ce2a03df00d39a4a4
```

O servidor valida esse campo e o devolve na resposta.

Se o cabeçalho estiver ausente, responde:
```
HTTP/1.1 400 Bad Request
```

---

## Estrutura de Rede Docker

A rede segue o padrão exigido pela matrícula (0840):
```
Sub-rede: 8.40.0.0/24
```

| Container    | IP        | Porta | Descrição                           |
|--------------|-----------|-------|-------------------------------------|
| client       | 8.40.0.2  | —     | Envia requisições e mede desempenho |
| seq_server   | 8.40.0.10 | 8080  | Servidor Sequencial                 |
| conc_server  | 8.40.0.11 | 8081  | Servidor Concorrente                |

---

## Como Executar o Projeto

### 1. Rodar tudo automaticamente

O projeto já possui o script `main.sh`, que automatiza toda a configuração:

- constrói as imagens
- cria a rede Docker com IPs da matrícula
- sobe os servidores
- executa o cliente
- gera o arquivo `resultados.csv`

Basta executar:
```bash
./main.sh
```

Durante a execução, o terminal exibirá logs semelhantes a:
```
🧱 Construindo containers...
🚀 Subindo servidores...
⏳ Aguardando servidores iniciarem (10s)...

==================== TESTANDO SERVIDOR Sequencial ====================
[8.40.0.10] GET 1/30 -> 0.00151s
...
✅ Resultados salvos em resultados/resultados.csv
📎 X-Custom-ID usado nas requisições: 8b33d991b6c4c6b80c1eec8ce2a03df00d39a4a4
```

### 2. Executar manualmente (opcional)

Caso queira subir e testar em etapas:
```bash
docker compose up --build
docker exec -it client bash
python3 client.py
```

Os resultados também serão salvos em:
```
resultados/resultados.csv
```

---

## Métricas Geradas

O cliente mede automaticamente o desempenho de cada requisição e calcula as seguintes métricas:

- **Tempo Médio (s)** — média aritmética dos tempos de resposta
- **Desvio Padrão (s)** — dispersão dos tempos em relação à média
- **Tempo Mínimo (s)** — menor tempo de resposta observado
- **Tempo Máximo (s)** — maior tempo de resposta observado
- **Throughput (req/s)** — número de requisições processadas por segundo

Exemplo do arquivo CSV gerado:
```csv
Servidor,Metodo,Media,DesvioPadrao,Min,Max,Throughput,N
Sequencial,GET,0.001500,0.000210,0.001200,0.001700,666.67,30
Concorrente,POST,0.000800,0.000150,0.000600,0.001000,1250.00,30
```

Essas informações são usadas no relatório para análise comparativa entre os dois servidores.

---

## Cabeçalhos HTTP incluídos

Os servidores retornam todos os cabeçalhos obrigatórios:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, X-Custom-ID
Access-Control-Expose-Headers: X-Custom-ID, Content-Type, Content-Length
```

Isso garante compatibilidade com diferentes clientes e facilita a integração.

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

**Reconstruir e executar:**
```bash
./main.sh
```

---

**Desenvolvido para a disciplina de Redes de Computadores II - UFPI**