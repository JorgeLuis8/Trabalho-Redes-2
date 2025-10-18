import socket, threading, hashlib

HOST, PORT = "0.0.0.0", 80

def gerar_custom_id():
    base = "20219040840 Jorge"
    return hashlib.sha1(base.encode()).hexdigest()

def montar_resposta(status, body):
    cid = gerar_custom_id()
    headers = (
        f"HTTP/1.1 {status}\r\n"
        f"X-Custom-ID: {cid}\r\n"
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, PUT, OPTIONS\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        "Connection: close\r\n\r\n"
    )
    return headers + body

def processar_requisicao(data):
    linha = data.split("\r\n")[0]
    metodo = linha.split(" ")[0]
    if metodo == "GET":
        return montar_resposta("200 OK", "<h1>Servidor Concorrente - GET</h1>")
    elif metodo == "POST":
        return montar_resposta("201 Created", "<h1>Servidor Concorrente - POST</h1>")
    elif metodo == "PUT":
        return montar_resposta("200 OK", "<h1>Servidor Concorrente - PUT</h1>")
    else:
        return montar_resposta("405 Method Not Allowed", "<h1>Método não suportado</h1>")

def handle_client(conn, addr):
    data = conn.recv(4096).decode()
    if data:
        resposta = processar_requisicao(data)
        conn.sendall(resposta.encode())
    conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    print(f"🚀 Servidor Concorrente ativo em {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
