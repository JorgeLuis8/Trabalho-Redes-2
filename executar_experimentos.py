import os, threading
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cliente import medir_rtt

PORTA = int(os.getenv("PORTA", 80))
N_EXEC = int(os.getenv("N_EXEC", 10))
CONC = int(os.getenv("CONC_CLIENTES", 50))

SERVS = {
    "sequencial": "servidor_sequencial",
    "concorrente": "servidor_concorrente",
}

CENARIOS = [
    ("GET /",       "/",    "GET",  b""),
    ("GET /info",   "/info","GET",  b""),
    ("GET /cpu",    "/cpu", "GET",  b""),
    ("GET /io",     "/io",  "GET",  b""),
    ("POST /echo",  "/echo","POST", b"hello sockets"),
]

def roda_seq(host, rotulo, path, method, body):
    tempos = [medir_rtt(host, path, method, body) for _ in range(N_EXEC)]
    return tempos

def roda_conc(host, rotulo, path, method, body):
    tempos = []
    lock = threading.Lock()
    def worker():
        t = medir_rtt(host, path, method, body)
        with lock:
            tempos.append(t)
    threads = [threading.Thread(target=worker) for _ in range(CONC)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    return tempos

def main():
    os.makedirs("resultados", exist_ok=True)
    linhas = []

    for nome_serv, host in SERVS.items():
        for (rotulo, path, method, body) in CENARIOS:
            # sequencial (N_EXEC)
            seq_ts = roda_seq(host, rotulo, path, method, body)
            linhas.append([nome_serv, rotulo, "sequencial", np.mean(seq_ts), np.std(seq_ts), len(seq_ts)])

            # concorrente (CONC threads simultâneas)
            conc_ts = roda_conc(host, rotulo, path, method, body)
            linhas.append([nome_serv, rotulo, "concorrente", np.mean(conc_ts), np.std(conc_ts), len(conc_ts)])

    df = pd.DataFrame(linhas, columns=["servidor","cenario","modo","media_s","desvio_s","n"])
    df.to_csv("resultados/metricas.csv", index=False)

    # gráfico por cenário comparando servidores
    for (rotulo, _, _, _) in CENARIOS:
        sub = df[df["cenario"]==rotulo]
        plt.figure()
        for modo in ["sequencial","concorrente"]:
            submodo = sub[sub["modo"]==modo]
            plt.bar(submodo["servidor"] + " " + modo, submodo["media_s"])
        plt.ylabel("Média do RTT (s)")
        plt.title(f"RTT médio por servidor — {rotulo} (N={N_EXEC}, CONC={CONC})")
        plt.xticks(rotation=15)
        plt.tight_layout()
        plt.savefig(f"resultados/{rotulo.strip('/').replace(' ','_') or 'root'}.png")
        plt.close()

    print("📊 Resultados salvos em:")
    print("- resultados/metricas.csv")
    print("- resultados/*.png")

if __name__ == "__main__":
    main()
