import socket, time, statistics, hashlib, os, csv

MATRICULA = "20219040840"
NOME = "Jorge"

SERVERS = [
    ("8.40.0.10", 80, "Sequencial"),
    ("8.40.0.11", 80, "Concorrente"),
]

def gerar_custom_id():
    base = f"{MATRICULA} {NOME}"
    return hashlib.sha1(base.encode()).hexdigest()

def montar_requisicao(metodo):
    xcid = gerar_custom_id()
    return (
        f"{metodo} / HTTP/1.1\r\n"
        "Host: servidor\r\n"
        "User-Agent: TestClient/1.0\r\n"
        f"X-Custom-ID: {xcid}\r\n"
        "Connection: close\r\n\r\n"
    )


def salvar_csv(resultados):
    os.makedirs("/app/resultados", exist_ok=True)
    with open("/app/resultados/resultados.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Servidor", "Método", "Média", "Desvio", "Min", "Max"])
        w.writerows(resultados)
    print("✅ Resultados salvos em resultados/resultados.csv")

def main():
    esperar_servidores()
    resultados = []

    for host, port, nome in SERVERS:
        print(f"\n==================== TESTANDO SERVIDOR {nome} ====================")
        for metodo in ["GET", "POST", "PUT"]:
            tempos = medir_tempo(host, port, metodo)
            if tempos:
                media = statistics.mean(tempos)
                desvio = statistics.pstdev(tempos)
                print(f"{nome}-{metodo}: Média={media:.5f}s | Min={min(tempos):.5f}s | Max={max(tempos):.5f}s | σ={desvio:.5f}s")
                resultados.append([nome, metodo, media, desvio, min(tempos), max(tempos)])

    salvar_csv(resultados)

def medir_tempo(host, port, metodo, n=30):  # 🔁 agora faz 30 testes
    tempos = []
    for i in range(n):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            inicio = time.time()
            s.connect((host, port))
            s.sendall(montar_requisicao(metodo).encode())
            while s.recv(4096):
                pass
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
    import socket, time
    servers = [("8.40.0.10", 80), ("8.40.0.11", 80)]
    print("⏳ Verificando disponibilidade dos servidores...", end="")
    for i in range(30):  # tenta por até 30s
        prontos = 0
        for host, port in servers:
            try:
                s = socket.socket()
                s.settimeout(1)
                s.connect((host, port))
                prontos += 1
                s.close()
            except:
                pass
        if prontos == len(servers):
            print(" ✅ Todos os servidores prontos!")
            return
        print(".", end="", flush=True)
        time.sleep(1)
    print("\n⚠️ Timeout: servidores não responderam em 30s.")


if __name__ == "__main__":
    main()
