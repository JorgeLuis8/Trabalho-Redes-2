import os, socket, time
from main import gerar_id_personalizado, CRLF

MATRICULA = os.getenv("MATRICULA")
NOME = os.getenv("NOME_ALUNO")
PORTA = int(os.getenv("PORTA", 80))
ID_CUSTOM = gerar_id_personalizado(MATRICULA, NOME)

def _send(host, path="/info", method="GET", body=b""):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, PORTA))
        headers = [
            f"{method} {path} HTTP/1.1",
            f"Host: {host}",
            f"X-Custom-ID: {ID_CUSTOM}",
            "Connection: close",
        ]
        if method == "POST":
            headers.append("Content-Type: text/plain; charset=utf-8")
            headers.append(f"Content-Length: {len(body)}")
        headers.append("")  # blank line
        req = CRLF.join(headers).encode("utf-8") + b"\r\n" + (body if method == "POST" else b"")
        s.sendall(req)
        # lê tudo (sem analisar resposta aqui)
        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk: break
            data += chunk
        return data

def medir_rtt(host, path="/info", method="GET", body=b""):
    ini = time.time()
    _send(host, path, method, body)
    fim = time.time()
    return fim - ini
