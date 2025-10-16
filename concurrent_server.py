import socket
import threading
import hashlib

HOST = "0.0.0.0"
PORT = 80

def gerar_custom_id():
    texto = "20219040840 Jorge"
    return hashlib.sha1(texto.encode()).hexdigest()

def montar_html(titulo, corpo):
    return f"""
    <html>
    <head>
        <title>{titulo}</title>
        <style>
            body {{ font-family: Arial; background-color: #f9f9f9; margin: 30px; color: #333; }}
            h1 {{ color: #008000; }}
        </style>
    </head>
    <body>
        <h1>{titulo}</h1>
        <p>{corpo}</p>
        <hr>
        <small><b>X-Custom-ID:</b> {gerar_custom_id()}</small>
    </body>
    </html>
    """

def montar_resposta_http(status_code, html, metodo="GET"):
    status_text = {
        200: "OK",
        201: "Created",
        204: "No Content",
        400: "Bad Request",
        404: "Not Found",
        500: "Internal Server Error"
    }.get(status_code, "OK")

    cors_headers = (
        "Access-Control-Allow-Origin: *\r\n"
        "Access-Control-Allow-Methods: GET, POST, PUT, OPTIONS\r\n"
        "Access-Control-Allow-Headers: Content-Type\r\n"
    )

    if metodo == "OPTIONS":
        return (
            f"HTTP/1.1 204 No Content\r\n"
            f"{cors_headers}"
            "Content-Length: 0\r\n"
            "Connection: close\r\n\r\n"
        ).encode()

    resposta = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"X-Custom-ID: {gerar_custom_id()}\r\n"
        f"{cors_headers}"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(html.encode())}\r\n"
        "Connection: close\r\n\r\n"
        f"{html}"
    )
    return resposta.encode()

def processar_requisicao(data):
    try:
        linha_inicial = data.split("\r\n")[0]
        metodo, _, _ = linha_inicial.split(" ")

        if metodo == "OPTIONS":
            return montar_resposta_http(204, "", metodo)

        elif metodo == "GET":
            html = montar_html("Servidor Concorrente - GET", "Recurso obtido com sucesso!")
            return montar_resposta_http(200, html)

        elif metodo == "POST":
            html = montar_html("Servidor Concorrente - POST", "Novo recurso criado com sucesso!")
            return montar_resposta_http(201, html)

        elif metodo == "PUT":
            html = montar_html("Servidor Concorrente - PUT", "Recurso atualizado com sucesso!")
            return montar_resposta_http(200, html)

        else:
            html = montar_html("Erro", f"Método {metodo} não suportado.")
            return montar_resposta_http(400, html)

    except Exception as e:
        html = montar_html("Erro Interno", str(e))
        return montar_resposta_http(500, html)

def handle_client(conn, addr):
    data = conn.recv(2048).decode()
    if data:
        print(f"\n===================== REQUISIÇÃO DE {addr} ======================")
        print(data)
        resposta = processar_requisicao(data)
        conn.sendall(resposta)
    conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"🚀 Servidor CONCORRENTE ativo em {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
