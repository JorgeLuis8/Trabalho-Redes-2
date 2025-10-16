import socket, time, statistics, csv, os

SERVERS = [
    ("172.40.0.10", 80, "Sequencial"),
    ("172.40.0.11", 80, "Concorrente")
]
METODOS = ["GET", "POST", "PUT"]

# 🔹 Garante que a pasta exista dentro do container
os.makedirs("/app/resultados", exist_ok=True)

def montar_requisicao(metodo):
    return f"{metodo} / HTTP/1.1\r\nHost: servidor\r\nUser-Agent: TestClient/1.0\r\nConnection: close\r\n\r\n"

def medir_tempo(host, port, metodo, n=10):
    tempos, cabecalhos = [], []
    for i in range(n):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            inicio = time.time()
            s.connect((host, port))
            s.sendall(montar_requisicao(metodo).encode())
            resposta = b""
            while True:
                parte = s.recv(4096)
                if not parte:
                    break
                resposta += parte
            fim = time.time()
            s.close()

            latencia = fim - inicio
            tempos.append(latencia)
            resposta_str = resposta.decode(errors="ignore")
            cabecalhos.append(resposta_str.split("\r\n\r\n")[0])

            print(f"[{host}] {metodo} {i+1}/{n} -> {latencia:.5f}s")

        except Exception as e:
            print(f"⚠️ Erro ({metodo}): {e}")
    return tempos, cabecalhos

def main():
    print("⏳ Aguardando servidores iniciarem (10s)...")
    time.sleep(10)
    resultados = []

    for host, port, tipo in SERVERS:
        print(f"\n==================== TESTANDO SERVIDOR {tipo} ====================")
        for metodo in METODOS:
            tempos, _ = medir_tempo(host, port, metodo)
            if tempos:
                media = statistics.mean(tempos)
                desvio = statistics.stdev(tempos) if len(tempos) > 1 else 0
                lat_min, lat_max = min(tempos), max(tempos)
                resultados.append([tipo, metodo, media, desvio, lat_min, lat_max])
                print(f"{tipo}-{metodo}: Média={media:.5f}s | Min={lat_min:.5f}s | Max={lat_max:.5f}s | σ={desvio:.5f}s")

    # 🔹 Corrigido — grava dentro da pasta resultados/
    with open("/app/resultados/resultados.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Servidor", "Metodo", "Media", "Desvio", "Min", "Max"])
        writer.writerows(resultados)
    print("✅ Resultados salvos em /app/resultados/resultados.csv")

if __name__ == "__main__":
    main()
