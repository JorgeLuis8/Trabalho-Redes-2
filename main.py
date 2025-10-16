import hashlib

CRLF = "\r\n"

def gerar_id_personalizado(matricula, nome):
    base = f"{matricula} {nome}".encode("utf-8")
    return hashlib.sha1(base).hexdigest()

def montar_resposta_http(status_code, mensagem, headers, body_bytes):
    linhas = [f"HTTP/1.1 {status_code} {mensagem}"]
    base_headers = {
        "Server": "UFPI-Sockets/1.0",
        "Content-Length": str(len(body_bytes)),
        "Connection": "close",
        "Content-Type": "text/plain; charset=utf-8",
    }
    base_headers.update(headers or {})
    for k, v in base_headers.items():
        linhas.append(f"{k}: {v}")
    linhas.append("")  # linha em branco
    cab = CRLF.join(linhas).encode("utf-8") + b"\r\n"
    return cab + body_bytes

def parse_http_request(sock):
    # lê cabeçalho até CRLF CRLF
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    header_part, _, rest = data.partition(b"\r\n\r\n")
    linhas = header_part.decode("utf-8", errors="replace").split(CRLF)
    reqline = linhas[0]
    metodo, caminho, versao = reqline.split(" ")
    headers = {}
    for ln in linhas[1:]:
        if not ln:
            continue
        if ":" in ln:
            k, v = ln.split(":", 1)
            headers[k.strip()] = v.strip()
    # corpo (se Content-Length)
    body = rest
    cl = int(headers.get("Content-Length", "0") or "0")
    while len(body) < cl:
        chunk = sock.recv(4096)
        if not chunk:
            break
        body += chunk
    return metodo, caminho, versao, headers, body
