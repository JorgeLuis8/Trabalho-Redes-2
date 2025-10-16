import time

def tratar_requisicao(metodo, caminho, body_bytes: bytes):
    # Cenários de carga para comparar servidores
    # 1) Rota simples
    if metodo == "GET" and caminho == "/":
        return 200, "OK", b"Servidor ativo!"

    # 2) Info
    if metodo == "GET" and caminho == "/info":
        return 200, "OK", b"Servidor Web com Sockets e HTTP"

    # 3) CPU-bound simulado
    if metodo == "GET" and caminho == "/cpu":
        # loop CPU para consumir ~30-50ms dependendo do host
        s = 0
        for i in range(1_000_00):
            s += (i % 7) * (i % 13)
        return 200, "OK", f"CPU sum={s}".encode()

    # 4) IO-bound simulado (latência artificial)
    if metodo == "GET" and caminho == "/io":
        time.sleep(0.05)  # 50ms
        return 200, "OK", b"IO OK (sleep 50ms)"

    # 5) POST ecoa corpo
    if metodo == "POST" and caminho == "/echo":
        return 200, "OK", body_bytes or b""

    return 404, "Not Found", b"Rota não encontrada"
