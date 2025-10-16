import os, socket
from main import gerar_id_personalizado, montar_resposta_http, parse_http_request
from main import CRLF
from rotas import tratar_requisicao

HOST, PORTA = "0.0.0.0", int(os.getenv("PORTA", 80))
ID_ESPERADO = gerar_id_personalizado(os.getenv("MATRICULA"), os.getenv("NOME_ALUNO"))

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORTA))
    s.listen(5)
    print(f"🚀 Servidor SEQUENCIAL ativo na porta {PORTA}")

    while True:
        conexao, addr = s.accept()
        try:
            metodo, caminho, versao, headers, body = parse_http_request(conexao)

            if headers.get("X-Custom-ID") != ID_ESPERADO:
                resp = montar_resposta_http(403, "Forbidden", {}, b"ID incorreto!")
            else:
                status, msg, corpo = tratar_requisicao(metodo, caminho, body)
                resp = montar_resposta_http(status, msg, {}, corpo)

            conexao.sendall(resp)
        except Exception as e:
            err = montar_resposta_http(500, "Internal Server Error", {}, str(e).encode())
            try: conexao.sendall(err)
            except: pass
        finally:
            conexao.close()

if __name__ == "__main__":
    main()
