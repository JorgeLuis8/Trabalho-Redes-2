import socket
import time
import statistics
import csv

SERVERS = [
    ("172.40.0.10", 80, "Sequencial"),
    ("172.40.0.11", 80, "Concorrente")
]

METODOS = ["GET", "POST", "PUT"]

def montar_requisicao(metodo):
    return (
        f"{metodo} / HTTP/1.1\r\n"
        "Host: servidor\r\n"
        "User-Agent: TestClient/1.0\r\n"
        "Connection: close\r\n\r\n"
    )

def medir_tempo(host, port, metodo, n=10):
    tempos = []
    cabecalhos = []
    for i in range(n):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            inicio = time.time()
            s.connect((host, port))
            s.sendall(montar_requisicao(metodo).encode())
            resposta = s.recv(4096).decode(errors="ignore")
            fim = time.time()
            s.close()

            header_part = resposta.split("\r\n\r\n")[0]
            cabecalhos.append(header_part)
            tempos.append(fim - inicio)
            print(f"[{host}] {metodo} {i+1}/{n} -> {fim - inicio:.5f}s")
        except Exception as e:
            print(f"⚠️ Erro ({metodo}): {e}")

    return tempos, cabecalhos

def main():
    print("⏳ Aguardando servidores iniciarem (10s)...")
    time.sleep(10)

    resultados = []
    metricas_totais = {}

    for host, port, tipo in SERVERS:
        print(f"\n==================== TESTANDO SERVIDOR {tipo} ====================")
        todos_tempos = []
        for metodo in METODOS:
            tempos, cabecalhos = medir_tempo(host, port, metodo)
            if tempos:
                media = statistics.mean(tempos)
                desvio = statistics.stdev(tempos) if len(tempos) > 1 else 0
                resultados.append((tipo, metodo, media, desvio))
                todos_tempos.extend(tempos)

                print("\n📋 Cabeçalho HTTP de exemplo:")
                print(cabecalhos[0])
                print("-------------------------------------------------------------")
                print(f"{tipo} - {metodo}: média={media:.5f}s | desvio={desvio:.5f}s")
                print("-------------------------------------------------------------\n")

        if todos_tempos:
            media_total = statistics.mean(todos_tempos)
            desvio_total = statistics.stdev(todos_tempos)
            metricas_totais[tipo] = (media_total, desvio_total)
            print(f"📊 MÉTRICAS TOTAIS ({tipo}): média={media_total:.5f}s | desvio={desvio_total:.5f}s\n")

    with open("resultados.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Servidor", "Metodo", "Media", "DesvioPadrao"])
        writer.writerows(resultados)
        writer.writerow([])
        writer.writerow(["Servidor", "MediaTotal", "DesvioTotal"])
        for tipo, (media, desvio) in metricas_totais.items():
            writer.writerow([tipo, f"{media:.5f}", f"{desvio:.5f}"])

    print("✅ Resultados salvos em resultados.csv")

if __name__ == "__main__":
    main()
