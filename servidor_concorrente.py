import os, socket, threading
from main import gerar_id_personalizado, montar_resposta_http, parse_http_request

HOST, PORTA = "0.0.0.0", int(os.getenv("PORTA", 80))
ID_ESPERADO = gerar_id_personalizado(os.getenv("MATRICULA"), os.getenv("NOME_ALUNO"))

def atender(conexao, addr):
    try:
        metodo, caminho, versao, headers, body = parse_http_request(conexao)
        if headers.get("X-Custom-ID") != ID_ESPERADO:
            resp = montar_resposta_http(403, "Forbidden", {}, b"ID incorreto!")
        else:
            from rotas import tratar_requisicao
            status, msg, corpo = tratar_requisicao(metodo, caminho, body)
            resp = montar_resposta_http(status, msg, {}, corpo)
        conexao.sendall(resp)
    except Exception as e:
        try:
            err = montar_resposta_http(500, "Internal Server Error", {}, str(e).encode())
            conexao.sendall(err)
        except:
            pass
    finally:
        conexao.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORTA))
    s.listen(128)
    print(f"🚀 Servidor CONCORRENTE ativo na porta {PORTA}")

    while True:
        c, addr = s.accept()
        t = threading.Thread(target=atender, args=(c, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    main()
