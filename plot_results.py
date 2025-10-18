import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carrega o CSV de resultados
df = pd.read_csv("resultados/resultados.csv")

# Ordena os métodos na ordem natural HTTP
ordem_metodos = ["GET", "POST", "PUT", "DELETE"]
df["Metodo"] = pd.Categorical(df["Metodo"], categories=ordem_metodos, ordered=True)
df = df.sort_values(["Metodo", "Servidor"])

# Cores e posição
largura = 0.35
metodos = df["Metodo"].unique()
x = np.arange(len(metodos))

# Extrai valores de cada servidor
seq = df[df["Servidor"] == "Sequencial"]["Media"]
conc = df[df["Servidor"] == "Concorrente"]["Media"]

plt.figure(figsize=(8,5))
plt.bar(x - largura/2, seq, largura, label="Sequencial", color="#ff9933")
plt.bar(x + largura/2, conc, largura, label="Concorrente", color="#3399ff")

# Rótulos de valor acima das barras
for i, v in enumerate(seq):
    plt.text(i - largura/2, v + 0.00002, f"{v:.4f}", ha='center', fontsize=8)
for i, v in enumerate(conc):
    plt.text(i + largura/2, v + 0.00002, f"{v:.4f}", ha='center', fontsize=8)

plt.xticks(x, metodos)
plt.ylabel("Latência média (s)")
plt.xlabel("Método HTTP")
plt.title("Comparação de desempenho – Servidor Sequencial vs Concorrente")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("resultados/grafico_comparativo.png", dpi=150)
plt.show()

print("✅ Gráfico salvo em resultados/grafico_comparativo.png")
