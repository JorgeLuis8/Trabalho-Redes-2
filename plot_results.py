import csv
import matplotlib.pyplot as plt

tipos, medias, desvios = [], [], []

with open("resultados.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        tipos.append(row["Tipo"])
        medias.append(float(row["Media"]))
        desvios.append(float(row["DesvioPadrao"]))

plt.figure(figsize=(6, 4))
plt.bar(tipos, medias, yerr=desvios, capsize=8)
plt.title("Comparação de Desempenho")
plt.ylabel("Tempo médio de resposta (s)")
plt.xlabel("Tipo de Servidor")
plt.grid(True, axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("grafico_resultados.png")
plt.show()

print("✅ Gráfico salvo como grafico_resultados.png")
