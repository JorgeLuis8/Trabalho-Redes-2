import csv
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import os

CSV_PATH = "resultados/resultados.csv"
OUT_PATH = "resultados/grafico_latency.png"

# Carrega CSV
data = defaultdict(dict)
with open(CSV_PATH, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        srv = row["Servidor"]
        metodo = row["Metodo"]
        media = float(row["Media"])
        desv = float(row["DesvioPadrao"])
        data[metodo][srv] = (media, desv)

metodos = ["GET", "POST", "PUT", "DELETE"]
servs = ["Sequencial", "Concorrente"]

# Monta gráfico de barras com barras de erro (σ)
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=140)
x = range(len(metodos))
width = 0.35

seq_means = [data[m].get("Sequencial", (0, 0))[0] for m in metodos]
seq_errs  = [data[m].get("Sequencial", (0, 0))[1] for m in metodos]
con_means = [data[m].get("Concorrente", (0, 0))[0] for m in metodos]
con_errs  = [data[m].get("Concorrente", (0, 0))[1] for m in metodos]

ax.bar([i - width/2 for i in x], seq_means, width, yerr=seq_errs, label="Sequencial", capsize=3)
ax.bar([i + width/2 for i in x], con_means, width, yerr=con_errs, label="Concorrente", capsize=3)

ax.set_xticks(list(x))
ax.set_xticklabels(metodos)
ax.set_ylabel("Latência média (s)")
ax.set_title("Comparativo de Latência — Média ± σ (N execuções)")
ax.legend()
ax.grid(axis="y", alpha=0.25)

os.makedirs("resultados", exist_ok=True)
plt.tight_layout()
plt.savefig(OUT_PATH)
print(f"✅ Gráfico salvo em {OUT_PATH}")
