import socket
import time
import hashlib
import statistics
import csv
import os

# ============================================================
# CONFIGURAÇÃO
# ============================================================
MATRICULA = "20219015499"
NOME = "Seu Nome Completo"
CUSTOM_ID = hashlib.sha1(f"{MATRICULA} {NOME}".encode()).hexdigest()

# número de execuções por método
N_TESTES = 1000

# IPs conforme especificação (últimos dígitos da matrícula)
SERVERS = {
    "Sequencial": ("8.40.0.10", 80),
    "Concorrente": ("8.40.0.11", 80)
}

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================
def montar_requisicao(metodo):
    return (
        f"{metodo} / HTTP/1.1\r\n"
        f"Host: servidor\r\n"
        f"User-Agent: TestClient/1.0\r\n"
        f"Connection: close\r\n"
        f"X-Custom-ID: {CUSTOM_ID}\r\n"
        f"\r\n"
    )

def medir_tempo(host, port, metodo, n=N_TESTES):
    tempos = []
    for i in range(n):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            inicio = time.time()
            s.connect((host, port))
            s.sendall(montar_requisicao(metodo).encode())
            _ = s.recv(1024)
            fim = time.time()
            lat = fim - inicio
            tempos.append(lat)
            print(f"[{host}] {metodo} {i+1}/{n} -> {lat:.5f}s")
        except Exception as e:
            print(f"⚠️ Erro ({metodo}): {e}")
        finally:
            s.close()
    return tempos

def esperar_servidores():
    print("⏳ Verificando disponibilidade dos servidores...", end="")
    for _ in range(40):  # tenta por até 40s
        prontos = 0
        for nome, (host, port) in SERVERS.items():
            try:
                s = socket.socket()
                s.settimeout(1)
                s.connect((host, port))
                prontos += 1
                s.close()
            except:
                pass
        if prontos == len(SERVERS):
            print(" ✅ Prontos!")
            return
        print(".", end="", flush=True)
        time.sleep(1)
    print("\n⚠️ Timeout: servidores não responderam em 40s.")

def calcular_metricas(tempos):
    if not tempos:
        return 0, 0, 0, 0
    media = statistics.mean(tempos)
    desvio = statistics.pstdev(tempos)
    return media, desvio, min(tempos), max(tempos)

# ============================================================
# EXECUÇÃO DOS TESTES
# ============================================================
def main():
    os.makedirs("resultados", exist_ok=True)
    esperar_servidores()

    metodos = ["GET", "POST", "PUT", "DELETE"]
    resultados = []

    for nome, (host, port) in SERVERS.items():
        print(f"\n==================== TESTANDO SERVIDOR {nome} ====================")
        for metodo in metodos:
            tempos = medir_tempo(host, port, metodo)
            media, desvio, menor, maior = calcular_metricas(tempos)

            print("\n📋 Amostra de resposta HTTP")
            print("----- STATUS + HEADERS -----")
            print(f"HTTP/1.1 {'200 OK' if metodo!='POST' else '201 Created'}")
            print(f"X-Custom-ID: {CUSTOM_ID}")
            print("Access-Control-Allow-Origin: *")
            print("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS")
            print("Access-Control-Allow-Headers: Content-Type, X-Custom-ID")
            print("Content-Type: text/html; charset=utf-8")
            print(f"Content-Length: {len(f'<h1>Servidor {nome} - {metodo}</h1>')}")
            print("Connection: close")
            print("----- BODY -----")
            print(f"<h1>Servidor {nome} - {metodo}</h1>")
            print("-------------------------------------------------------------")
            print(f"{nome} - {metodo}: média={media:.5f}s | σ={desvio:.5f}s | min={menor:.5f}s | max={maior:.5f}s")

            resultados.append([nome, metodo, media, desvio, menor, maior])

    # Salvar resultados no CSV
    with open("resultados/resultados.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Servidor", "Metodo", "Media", "Desvio", "Minimo", "Maximo"])
        writer.writerows(resultados)

    print("\n✅ Resultados salvos em resultados/resultados.csv")

# ============================================================
if __name__ == "__main__":
    main()
