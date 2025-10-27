import socket
import threading
from email.utils import formatdate  # gera Date em RFC 1123

HOST = "0.0.0.0"
PORT = 80
ALLOWED = {"GET", "POST", "PUT", "DELETE", "OPTIONS"}

# 🔧 Cabeçalhos base (CORS + identidade) aplicados em TODAS as respostas
BASE_HEADERS = {
    "Server": "Concorrente/1.0",
    "Connection": "close",

    # CORS
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, X-Custom-ID",

    # Expor no fetch() tudo que queremos enxergar no front
    "Access-Control-Expose-Headers": (
        "X-Custom-ID, Content-Type, Content-Length, Date, Server, "
        "Access-Control-Allow-Origin, Access-Control-Allow-Methods, "
        "Access-Control-Allow-Headers, Access-Control-Expose-Headers, Allow"
    ),
}

def http_response(status_line: str, headers: dict, body: str = "") -> bytes:
    """
    Monta uma resposta HTTP consistente:
      - Adiciona Date, Server, Connection.
      - Aplica CORS e lista de exposed headers.
      - Garante Content-Length e Content-Type coerentes.
    """
    out = dict(headers or {})
    out["Date"] = formatdate(usegmt=True)  # sempre atual
    for k, v in BASE_HEADERS.items():
        out.setdefault(k, v)

    if body:
        out["Content-Type"] = out.get("Content-Type", "text/html; charset=utf-8")
        out["Content-Length"] = str(len(body.encode("utf-8")))
    else:
        out["Content-Length"] = out.get("Content-Length", "0")
        out.setdefault("Content-Type", "text/html; charset=utf-8")

    head = status_line + "\r\n" + "".join(f"{k}: {v}\r\n" for k, v in out.items()) + "\r\n"
    return (head + (body or "")).encode("utf-8")


def build_ok(method: str, xcid: str) -> bytes:
    body = f"<h1>Servidor Concorrente - {method}</h1>"
    return http_response("HTTP/1.1 200 OK", {"X-Custom-ID": xcid}, body)


def build_bad_request(msg: str) -> bytes:
    body = f"<h1>400 Bad Request</h1><p>{msg}</p>"
    return http_response("HTTP/1.1 400 Bad Request", {}, body)


def build_method_not_allowed() -> bytes:
    body = "<h1>405 Method Not Allowed</h1>"
    return http_response(
        "HTTP/1.1 405 Method Not Allowed",
        {"Allow": ", ".join(sorted(ALLOWED))},
        body
    )


def build_options(xcid: str) -> bytes:
    # Preflight sem corpo; cacheia por 10 min
    return http_response(
        "HTTP/1.1 204 No Content",
        {
            "X-Custom-ID": xcid,
            "Allow": ", ".join(sorted(ALLOWED)),
            "Access-Control-Max-Age": "600",
        },
        body=""
    )


def handle(conn: socket.socket, addr):
    print(f"🧵 {threading.current_thread().name} atendendo {addr}")
    try:
        conn.settimeout(5.0)
        data = conn.recv(16384).decode(errors="ignore")
        if not data:
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
    except Exception as e:
        # Resposta simples em caso de erro inesperado
        try:
            conn.sendall(http_response("HTTP/1.1 500 Internal Server Error", {}, f"<h1>500</h1><p>{e}</p>"))
        except Exception:
            pass
    finally:
        try:
            conn.shutdown(socket.SHUT_WR)
        except Exception:
            pass
        conn.close()


def main():
    print(f"🚀 Servidor Concorrente (threads) em {HOST}:{PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(128)

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
