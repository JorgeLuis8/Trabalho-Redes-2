import socket
from email.utils import formatdate  # para gerar 'Date' RFC 1123

HOST = "0.0.0.0"
PORT = 80
ALLOWED = {"GET", "POST", "PUT", "DELETE", "OPTIONS"}

# 🔧 Cabeçalhos CORS e de servidor usados em TODAS as respostas
BASE_HEADERS = {
    # Identidade do servidor + conexão
    "Server": "Sequencial/1.0",
    "Connection": "close",

    # CORS (permite o fetch do browser ver os cabeçalhos abaixo)
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, X-Custom-ID",
    # Liste aqui TUDO que você deseja ler via resp.headers.* no front
    "Access-Control-Expose-Headers": (
        "X-Custom-ID, Content-Type, Content-Length, Date, Server, "
        "Access-Control-Allow-Origin, Access-Control-Allow-Methods, "
        "Access-Control-Allow-Headers, Access-Control-Expose-Headers, Allow"
    ),
}

def http_response(status_line: str, headers: dict, body: str = "") -> bytes:
    """
    Monta resposta HTTP.
    - Garante Date/Server/Connection.
    - Aplica CORS e lista de exposed headers.
    - Garante Content-Length e Content-Type coerentes (text/html).
    """
    # copia para não mutar o dicionário recebido
    out_headers = dict(headers or {})
    # sempre define Date atual
    out_headers["Date"] = formatdate(usegmt=True)
    # aplica base (CORS + server + connection)
    for k, v in BASE_HEADERS.items():
        out_headers.setdefault(k, v)

    # Se houver body, define tipo e tamanho
    if body:
        out_headers["Content-Type"] = out_headers.get("Content-Type", "text/html; charset=utf-8")
        out_headers["Content-Length"] = str(len(body.encode("utf-8")))
    else:
        # Sem body → tamanho 0 (inclusive para 204)
        out_headers["Content-Length"] = out_headers.get("Content-Length", "0")
        # definir Content-Type não é obrigatório sem body, mas não faz mal:
        out_headers.setdefault("Content-Type", "text/html; charset=utf-8")

    # monta head+body
    head = status_line + "\r\n" + "".join(f"{k}: {v}\r\n" for k, v in out_headers.items()) + "\r\n"
    return (head + (body or "")).encode("utf-8")


def build_ok(method: str, xcid: str) -> bytes:
    body = f"<h1>Servidor Sequencial - {method}</h1>"
    headers = {"X-Custom-ID": xcid}
    return http_response("HTTP/1.1 200 OK", headers, body)


def build_bad_request(msg: str) -> bytes:
    body = f"<h1>400 Bad Request</h1><p>{msg}</p>"
    return http_response("HTTP/1.1 400 Bad Request", {}, body)


def build_method_not_allowed() -> bytes:
    body = "<h1>405 Method Not Allowed</h1>"
    # Inclui Allow para deixar claro o que é aceito
    return http_response(
        "HTTP/1.1 405 Method Not Allowed",
        {"Allow": ", ".join(sorted(ALLOWED))},
        body
    )


def build_options(xcid: str) -> bytes:
    # Preflight / OPTIONS: sem corpo, mas com Allow + Max-Age para navegadores
    headers = {
        "X-Custom-ID": xcid,
        "Allow": ", ".join(sorted(ALLOWED)),
        "Access-Control-Max-Age": "600",  # 10 min de cache do preflight
    }
    # 204 No Content, Content-Length: 0
    return http_response("HTTP/1.1 204 No Content", headers, body="")

def handle(conn, addr):
    data = conn.recv(16384).decode(errors="ignore")
    if not data:
        conn.close()
        return

    lines = data.split("\r\n")
    request_line = lines[0] if lines else ""
    parts = request_line.split()
    method = parts[0] if len(parts) >= 1 else "GET"

    # Extrai X-Custom-ID
    xcid = None
    for line in lines[1:]:
        if line.lower().startswith("x-custom-id:"):
            xcid = line.split(":", 1)[1].strip()
            break

    if method not in ALLOWED:
        resp = build_method_not_allowed()
    elif method == "OPTIONS":
        resp = build_options(xcid or "N/A")
    elif not xcid:
        resp = build_bad_request("Cabeçalho obrigatório X-Custom-ID ausente.")
    else:
        resp = build_ok(method, xcid)

    conn.sendall(resp)
    conn.close()


def main():
    print(f"🌐 Servidor Sequencial (síncrono) em {HOST}:{PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(32)
    while True:
        conn, addr = s.accept()
        handle(conn, addr)


if __name__ == "__main__":
    main()
