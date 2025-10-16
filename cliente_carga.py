import os, socket, json, threading, time, statistics
from queue import Queue
from urllib.parse import urlencode
from main import gerar_id_personalizado, CRLF

def montar_requisicao(ip: str, metodo: str, caminho="/eco?msg=teste", corpo=b""):
    xcustom = gerar_id_personalizado(os.getenv("MATRICULA"), os.getenv("NOME_ALUNO"), os.getenv("ALGORITMO_HASH","md5"))
    headers = [
        f"{metodo} {caminho} HTTP/1.1",
        f"Host: {ip}",
        f"X-Custom-ID: {xcustom}",
        "Connection: close",
    ]
    if corpo:
        headers += [f"Content-Type: application/json; charset=utf-8", f"Content-Length: {len(corpo)}"]
    req = (CRLF.join(headers) + CRLF + CRLF).encode("utf-8") + (corpo or b"")
    # imprime cabeçalhos de requisição uma vez
    print("=== Requisição (headers) ===")
    print((CRLF.join(headers)).encode("utf-8").decode())
    return req

def fazer_req(ip: str, porta: int, req: bytes):
    t0 = time.perf_counter_ns()
    with socket.create_connection((ip, porta), timeout=5.0) as s:
        s.sendall(req)
        buff = b""
        while True:
            c = s.recv(65536)
            if not c: break
            buff += c
    t1 = time.perf_counter_ns()
    return buff, (t1 - t0)/1_000_000.0

def worker(q: Queue, resultados: list):
    while True:
        item = q.get()
        if item is None: break
        ip, porta, req = item
        try:
            resp, lat = fazer_req(ip, porta, req)
            # imprime cabeçalho de resposta só da primeira resposta de cada thread
            if lat is not None and q.unfinished_tasks == 0:
                head = resp.split((CRLF*2).encode(),1)[0].decode("utf-8","ignore")
                print("=== Resposta (headers) ===")
                print(head)
            resultados.append(("ok", lat))
        except Exception:
            resultados.append(("err", None))
        finally:
            q.task_done()

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--ip", required=True)
    p.add_argument("--porta", type=int, default=int(os.getenv("PORTA_SERVIDOR","80")))
    p.add_argument("--modo", choices=["GET","POST"], default="GET")
    p.add_argument("--concor", type=int, default=10)
    p.add_argument("--reqs", type=int, default=100)
    args = p.parse_args()

    if args.modo == "GET":
        caminho = "/eco?" + urlencode({"msg":"teste"})
        corpo = None
    else:
        caminho = "/soma"
        corpo = json.dumps({"a": 10, "b": 5}).encode("utf-8")

    req = montar_requisicao(args.ip, args.modo, caminho, corpo)

    q = Queue()
    resultados = []
    threads = [threading.Thread(target=worker, args=(q, resultados), daemon=True) for _ in range(args.concor)]
    for t in threads: t.start()

    t0 = time.time()
    for _ in range(args.reqs):
        q.put((args.ip, args.porta, req))
    q.join()
    t1 = time.time()
    for _ in threads: q.put(None)
    for t in threads: t.join()

    lats = [x for (st,x) in resultados if st=="ok" and x is not None]
    erros = sum(1 for (st,_) in resultados if st=="err")
    thr = len(resultados) / max(1e-9, (t1 - t0))
    saida = {
        "ok": len(lats), "erros": erros,
        "throughput_req_s": round(thr,2),
        "lat_ms_media": round(statistics.mean(lats),3) if lats else None,
        "lat_ms_dp": round(statistics.pstdev(lats),3) if lats else None,
        "lat_ms_p95": round(sorted(lats)[int(0.95*len(lats))-1],3) if lats else None
    }
    print(json.dumps(saida, ensure_ascii=False))

if __name__ == "__main__":
    main()
