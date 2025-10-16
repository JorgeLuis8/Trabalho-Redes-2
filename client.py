import socket
import time

SERVERS = [("8.40.0.10", 80), ("8.40.0.11", 80)]  # seq e conc
REQUISICAO = (
    "GET / HTTP/1.1\r\n"
    "Host: servidor\r\n"
    "User-Agent: TestClient/1.0\r\n"
    "Connection: close\r\n"
    "\r\n"
)

for host, port in SERVERS:
    start = time.time()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(REQUISICAO.encode())
    resposta = s.recv(4096).decode()
    s.close()
    end = time.time()
    print(f"Resposta de {host}:")
    print(resposta)
    print(f"Tempo: {end - start:.5f}s\n")
