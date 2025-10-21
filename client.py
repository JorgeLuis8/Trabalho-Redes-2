import socket
import time
import statistics
import os
import hashlib

# ===== Identificação exigida =====
MATRICULA = "20219040840"
NOME = "Jorge Luis Ferreira Luz"
CUSTOM_ID = hashlib.sha1(f"{MATRICULA} {NOME}".encode()).hexdigest()

# ===== Alvos na rede Docker 8.40.0.0/24 =====
TARGETS = {
    "Sequencial": ("8.40.0.10", 80),
    "Concorrente": ("8.40.0.11", 80),
}

METHODS = ["GET", "POST", "PUT", "DELETE"]
N_RUNS = int(os.getenv("N_RUNS", "30"))

os.makedirs("resultados", exist_ok=True)
CSV_PATH = "resultados/resultados.csv"

def http_request(method: str, host: str, port: int, body: bytes = b"") -> bytes:
    """Monta e envia uma requisição HTTP 'na mão' via sockets TCP, retorna bytes da resposta."""
    req_lines = [
        f"{method} / HTTP/1.1",
        f"Host: {host}",
        "User-Agent: SocketClient/1.0",
        f"X-Custom-ID: {CUSTOM_ID}",
        "Connection: close",
    ]
    if method in ("POST", "PUT"):
        req_lines.append("Content-Type: text/plain")
        req_lines.append(f"Content-Length: {len(body)}")
        payload = ("\r\n".join(req_lines) + "\r\n\r\n").encode() + body
    else:
        payload = ("\r\n".join(req_lines) + "\r\n\r\n").encode()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((host, port))
        s.sendall(payload)
        chunks = []
        while True:
            try:
                part = s.recv(4096)
            except socket.timeout:
                break
            if not part:
                break
            chunks.append(part)
    return b"".join(chunks)

def wait_ready():
    print("⏳ Verificando disponibilidade dos servidores...")
    deadline = time.time() + 20
    ready = {"Sequencial": False, "Concorrente": False}
    while time.time() < deadline and not all(ready.values()):
        for name, (h, p) in TARGETS.items():
            if ready[name]:
                continue
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1.0)
                    s.connect((h, p))
                    ready[name] = True
            except Exception:
                pass
        time.sleep(0.3)
    print("✅ Servidores prontos!" if all(ready.values()) else "⚠️ Prosseguindo mesmo assim...")

def print_sample(resp_bytes: bytes):
    try:
        txt = resp_bytes.decode(errors="ignore")
        head, _, body = txt.partition("\r\n\r\n")
        print("\n📋 Amostra de resposta HTTP")
        print("----- STATUS + HEADERS -----")
        for line in head.split("\r\n")[:12]:
            print(line)
        print("----- BODY -----")
        print(body.strip()[:200])
        print("-------------------------------------------------------------")
    except Exception as e:
        print(f"(Erro ao decodificar amostra: {e})")

def main():
    wait_ready()
    with open(CSV_PATH, "w", encoding="utf-8") as f:
        f.write("Servidor,Metodo,Media,DesvioPadrao,Min,Max,N\n")

    for srv_name, (host, port) in TARGETS.items():
        print(f"\n==================== TESTANDO SERVIDOR {srv_name} ====================")
        for method in METHODS:
            times = []
            amostra = None
            for i in range(N_RUNS):
                try:
                    t0 = time.perf_counter()
                    body = b"mensagem de teste" if method in ("POST", "PUT") else b""
                    resp = http_request(method, host, port, body=body)
                    dt = time.perf_counter() - t0
                    times.append(dt)
                    if amostra is None:
                        amostra = resp
                    print(f"[{host}] {method} {i+1}/{N_RUNS} -> {dt:.5f}s")
                except Exception as e:
                    print(f"⚠️ Erro ({method}): {e}")
            if amostra:
                print_sample(amostra)
            if times:
                media = sum(times) / len(times)
                desvio = statistics.pstdev(times)
                print(f"{srv_name} - {method}: média={media:.5f}s | σ={desvio:.5f}s | min={min(times):.5f}s | max={max(times):.5f}s")
                with open(CSV_PATH, "a", encoding="utf-8") as f:
                    f.write(f"{srv_name},{method},{media:.6f},{desvio:.6f},{min(times):.6f},{max(times):.6f},{len(times)}\n")

    print(f"\n✅ Resultados salvos em {CSV_PATH}")
    print("📎 X-Custom-ID usado:", CUSTOM_ID)

if __name__ == "__main__":
    main()
