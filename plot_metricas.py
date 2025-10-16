import pandas as pd
import matplotlib.pyplot as plt
import sys, os
from pathlib import Path

def main(csv_path: str):
    df = pd.read_csv(csv_path)
    outdir = Path("resultados")
    outdir.mkdir(parents=True, exist_ok=True)

    grp = df.groupby("cenario").agg(
        thr_media=("throughput_req_s","mean"),
        thr_dp=("throughput_req_s","std"),
        lat_media=("lat_ms_media","mean"),
        lat_dp=("lat_ms_media","std"),
        lat_p95=("lat_ms_p95","mean"),
        taxa_erro=("erros", lambda x: (x.sum())/ (df.loc[x.index,"reqs"].sum()))
    ).reset_index()

    resumo = outdir / ("resumo_" + Path(csv_path).name)
    grp.to_csv(resumo, index=False)
    print(f"[RESUMO] {resumo}")

    # Throughput
    plt.figure()
    plt.bar(grp["cenario"], grp["thr_media"], yerr=grp["thr_dp"])
    plt.xticks(rotation=25, ha="right"); plt.ylabel("Throughput (req/s)"); plt.title("Throughput médio por cenário"); plt.tight_layout()
    p1 = outdir / ("throughput_" + Path(csv_path).stem + ".png"); plt.savefig(p1); print(f"[PNG] {p1}")

    # Latência média
    plt.figure()
    plt.bar(grp["cenario"], grp["lat_media"], yerr=grp["lat_dp"])
    plt.xticks(rotation=25, ha="right"); plt.ylabel("Latência média (ms)"); plt.title("Latência média por cenário"); plt.tight_layout()
    p2 = outdir / ("lat_media_" + Path(csv_path).stem + ".png"); plt.savefig(p2); print(f"[PNG] {p2}")

    # Latência p95
    plt.figure()
    plt.bar(grp["cenario"], grp["lat_p95"])
    plt.xticks(rotation=25, ha="right"); plt.ylabel("Latência p95 (ms)"); plt.title("Latência p95 por cenário"); plt.tight_layout()
    p3 = outdir / ("lat_p95_" + Path(csv_path).stem + ".png"); plt.savefig(p3); print(f"[PNG] {p3}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: python3 plot_metricas.py resultados/metricas_YYYYMMDD_HHMMSS.csv")
        sys.exit(1)
    main(sys.argv[1])
