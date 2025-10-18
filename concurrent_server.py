import socket, threading, hashlib

HOST, PORT = "0.0.0.0", 80

def gerar_custom_id():
    base = "20219040840 Jorge"
    return hashlib.sha1(base.encode()).hexdigest()

def resposta_http(status, body):
    headers = (
        f"HTTP/1.1 {status}\r\n"
        f"X-Custom-ID: {gerar_custom_id()}\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS\r\n"
        "Access-Control-Allow-Headers: Content-Type, X-Custom-ID\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        "Connection: close\r\n\r\n"
    )
    return (headers + body).encode()

def processar(data: str) -> bytes:
    linha = data.split("\r\n")[0]
    metodo = (linha.split(" ") + ["", ""])[0]

    if metodo == "OPTIONS":
        return resposta_http("204 No Content", "")
    if metodo == "GET":
        return resposta_http("200 OK", "<h1>Servidor Concorrente - GET</h1>")
    if metodo == "POST":
        return resposta_http("201 Created", "<h1>Servidor Concorrente - POST</h1>")
    if metodo == "PUT":
        return resposta_http("200 OK", "<h1>Servidor Concorrente - PUT</h1>")
    if metodo == "DELETE":
        return resposta_http("200 OK", "<h1>Servidor Concorrente - DELETE</h1>")
    return resposta_http("405 Method Not Allowed", "<h1>Método não suportado</h1>")

def handle(conn, addr):
    data = conn.recv(8192).decode(errors="ignore")
    if data:
        conn.sendall(processar(data))
    conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(64)
    print(f"🚀 Servidor CONCORRENTE ativo em {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
