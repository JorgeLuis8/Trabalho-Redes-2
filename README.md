# 🧠 Projeto: Servidores HTTP Sequencial e Concorrente

Trabalho desenvolvido para a disciplina **Redes de Computadores II (UFPI, 2025-2)**.  
O objetivo é comparar o desempenho entre dois servidores HTTP implementados em **Python com Sockets TCP**:
- Um **sequencial**, que atende um cliente por vez.
- Um **concorrente**, que usa **threads** para múltiplas conexões simultâneas.

---

## 🚀 Como Executar

### 1️⃣ Clonar e acessar a pasta
```bash
git clone <seu-repo>
cd Trabalho-Redes-2
2️⃣ Dar permissão de execução ao script
chmod +x run_tests.sh

3️⃣ Executar tudo de uma vez
./run_tests.sh


O script irá:

Limpar containers e redes antigas

Buildar todos os containers

Subir os servidores sequencial e concorrente

Rodar o cliente com 10 requisições de GET, POST e PUT

Calcular métricas de latência (média, mínima, máxima e desvio padrão)

Gerar o arquivo resultados.csv