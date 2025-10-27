import socket
import threading

HOST = "0.0.0.0"
PORT = 80
ALLOWED = {"GET", "POST", "PUT", "DELETE", "OPTIONS"}


def http_response(status_line: str, headers: dict, body: str = "") -> bytes:
    # 🔹 Cabeçalhos CORS obrigatórios
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-Custom-ID",
        "Access-Control-Expose-Headers": "X-Custom-ID, Content-Type, Content-Length",
    }
    headers.update(cors_headers)

    head = status_line + "\r\n" + "".join(f"{k}: {v}\r\n" for k, v in headers.items())
    if body:
        head += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        head += "Content-Type: text/html; charset=utf-8\r\n"
    head += "Connection: close\r\n\r\n"
    return (head + body).encode("utf-8")


def build_ok(method: str, xcid: str) -> bytes:
    body = f"<h1>Servidor Concorrente - {method}</h1>"
    headers = {"X-Custom-ID": xcid}
    return http_response("HTTP/1.1 200 OK", headers, body)


def build_bad_request(msg: str) -> bytes:
    body = f"<h1>400 Bad Request</h1><p>{msg}</p>"
    return http_response("HTTP/1.1 400 Bad Request", {}, body)


def build_method_not_allowed() -> bytes:
    body = "<h1>405 Method Not Allowed</h1>"
    return http_response("HTTP/1.1 405 Method Not Allowed", {}, body)


def build_options(xcid: str) -> bytes:
    return http_response("HTTP/1.1 204 No Content", {"X-Custom-ID": xcid})


def handle(conn, addr):
    print(f"🧵 Thread {threading.current_thread().name} atendendo {addr}")

    try:
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
    finally:
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
