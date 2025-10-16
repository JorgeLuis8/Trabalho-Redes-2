🧠 Projeto — Servidores HTTP Sequencial e Concorrente

Este projeto foi desenvolvido como parte da Segunda Avaliação de Redes de Computadores II, com o objetivo de comparar o desempenho entre um servidor web sequencial e um servidor concorrente.
Ambos foram implementados em Python com sockets TCP, respeitando o protocolo HTTP/1.1, e simulados via Docker.

📁 Estrutura do Projeto
Trabalho-Redes-2/
│
├── sequential_server.py      # Servidor sequencial (atende 1 cliente por vez)
├── concurrent_server.py      # Servidor concorrente (usa threads)
├── test_metrics.py           # Cliente de testes com métricas
├── index.html                # Interface web de teste (GET, POST, PUT)
├── docker-compose.yml        # Configuração do ambiente Docker
└── README.md                 # Este arquivo

⚙️ Pré-requisitos

Antes de rodar o projeto, você precisa ter instalado:

Docker

Docker Compose

Navegador web (Chrome, Edge, Firefox etc.)

Python 3 (opcional, apenas se quiser rodar test_metrics.py fora do container)

🚀 Passo a Passo — Rodando os Servidores
1️⃣ Subir os containers

No terminal, dentro da pasta do projeto:

docker compose up --build


Isso irá:

Criar e iniciar o servidor sequencial (porta 8080)

Criar e iniciar o servidor concorrente (porta 8081)

Você verá algo como:

🌐 Servidor SEQUENCIAL ativo em 0.0.0.0:80
🚀 Servidor CONCORRENTE ativo em 0.0.0.0:80

2️⃣ Testar pelo navegador (HTML)

Abra o arquivo index.html diretamente no seu computador:

Clique duas vezes no arquivo
ou

Clique com o botão direito → “Abrir com” → selecione seu navegador

A página mostrará dois blocos:

🟦 Servidor Sequencial (localhost:8080)
🟩 Servidor Concorrente (localhost:8081)

Cada bloco possui três botões:

Botão	Método HTTP	Descrição
🔵 GET	Retorna um recurso (página HTML simples)	
🟢 POST	Cria um novo recurso	
🟠 PUT	Atualiza um recurso existente	
3️⃣ Visualizar respostas

Ao clicar em qualquer botão, você verá:

O método usado

O servidor acessado

O status HTTP

E o conteúdo HTML completo retornado, incluindo o cabeçalho X-Custom-ID.

Exemplo de resposta exibida:

Método: GET
Servidor: http://localhost:8080
Status: 200 OK
Resposta:
HTTP/1.1 200 OK
X-Custom-ID: 0d7d404acf277354d4a7b7125f71920047444512
Access-Control-Allow-Origin: *
Content-Type: text/html; charset=utf-8
Content-Length: 285
Connection: close
<html>...</html>

🧮 Executando os testes de métricas

Após rodar os servidores, abra outro terminal e execute:

docker compose run --rm client


(ou se preferir, fora do Docker, use python test_metrics.py)

O script irá:

Enviar 10 requisições de cada tipo (GET, POST, PUT) para cada servidor.

Calcular média e desvio padrão de tempo de resposta.

Exibir os cabeçalhos HTTP reais.

Gerar o arquivo resultados.csv com todas as métricas.