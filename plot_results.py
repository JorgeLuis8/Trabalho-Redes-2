import csv
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")  # Para ambientes sem GUI
import matplotlib.pyplot as plt
import os

CSV_PATH = "resultados/resultados.csv"
OUT_PATH_LAT = "resultados/grafico_latency.png"
OUT_PATH_THR = "resultados/grafico_throughput.png"

# ===== Carrega CSV =====
data = defaultdict(dict)
throughput_data = defaultdict(dict)

with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        srv = row["Servidor"]
        metodo = row["Metodo"]
        media = float(row["Media"])
        desv = float(row["DesvioPadrao"])
        thr = float(row["Throughput"])
        data[metodo][srv] = (media, desv)
        throughput_data[metodo][srv] = thr

metodos = ["GET", "POST", "PUT", "DELETE"]
x = range(len(metodos))
width = 0.35

# ===== Gráfico 1 — Latência =====
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=140)
seq_means = [data[m].get("Sequencial", (0, 0))[0] for m in metodos]
seq_errs = [data[m].get("Sequencial", (0, 0))[1] for m in metodos]
con_means = [data[m].get("Concorrente", (0, 0))[0] for m in metodos]
con_errs = [data[m].get("Concorrente", (0, 0))[1] for m in metodos]

ax.bar([i - width/2 for i in x], seq_means, width, yerr=seq_errs, label="Sequencial", capsize=3)
ax.bar([i + width/2 for i in x], con_means, width, yerr=con_errs, label="Concorrente", capsize=3)
ax.set_xticks(list(x))
ax.set_xticklabels(metodos)
ax.set_ylabel("Latência média (s)")
ax.set_title("Comparativo de Latência — Média ± σ")
ax.legend()
ax.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(OUT_PATH_LAT)

# ===== Gráfico 2 — Throughput =====
fig, ax2 = plt.subplots(figsize=(8, 4.5), dpi=140)
seq_thr = [throughput_data[m].get("Sequencial", 0) for m in metodos]
con_thr = [throughput_data[m].get("Concorrente", 0) for m in metodos]

ax2.bar([i - width/2 for i in x], seq_thr, width, label="Sequencial")
ax2.bar([i + width/2 for i in x], con_thr, width, label="Concorrente")
ax2.set_xticks(list(x))
ax2.set_xticklabels(metodos)
ax2.set_ylabel("Throughput (req/s)")
ax2.set_title("Comparativo de Throughput — Requisições por Segundo")
ax2.legend()
ax2.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig(OUT_PATH_THR)

print(f"✅ Gráficos salvos em:\n - {OUT_PATH_LAT}\n - {OUT_PATH_THR}")
