"""Eksperimen D05/D07: perbandingan akurasi-waktu, skalabilitas, dan hasil per skenario.

Jalankan: python scripts/run_experiments.py   (sekitar 1-2 menit)
Keluaran: outputs/experiment_*.csv, outputs/experiment_report.md, outputs/figures/*.png
"""
import csv
import math
import random
import statistics as st
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from rute.cli import load_scenarios  # noqa: E402
from rute.dijkstra import dijkstra  # noqa: E402
from rute.graph import Graph, load_graph  # noqa: E402
from rute.tsp import build_matrix, held_karp, nearest_neighbor, solve, tour_cost, two_opt  # noqa: E402
from rute.viz import plot_route  # noqa: E402

OUT = ROOT / "outputs"
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)


def timed(fn, *a, repeat=1, **k):
    best, res = float("inf"), None
    for _ in range(repeat):
        t = time.perf_counter()
        res = fn(*a, **k)
        best = min(best, time.perf_counter() - t)
    return res, best


def write_csv(name, header, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def exp_comparison(g):
    """Submasalah sama (TSP): HK vs NN vs NN+2opt pada subset acak lokasi Jakarta."""
    rows = []
    for k in range(5, 16):
        reps = 10 if k <= 11 else 5 if k <= 13 else 3 if k == 14 else 2
        rng = random.Random(1000 + k)
        for r in range(reps):
            stops = rng.sample(range(1, 42), k)
            d, _ = build_matrix(g, [0] + stops)
            (opt, _), t_hk = timed(held_karp, d)
            nn, t_nn = timed(nearest_neighbor, d)
            (t2, _), t_2 = timed(lambda: two_opt(d, nn))
            c_nn, c_2 = tour_cost(d, nn), tour_cost(d, t2)
            c_in = tour_cost(d, list(range(k + 1)))
            rows.append([k, r, round(c_in, 3), round(c_nn, 3), round(c_2, 3), round(opt, 3),
                         round(t_nn * 1e3, 4), round(t_2 * 1e3, 4), round(t_hk * 1e3, 3)])
    write_csv("experiment_comparison.csv",
              ["k_stops", "instance", "cost_input", "cost_nn", "cost_nn2opt", "cost_optimal",
               "ms_nn", "ms_2opt", "ms_heldkarp"], rows)
    summary = []
    for k in sorted({r[0] for r in rows}):
        rs = [r for r in rows if r[0] == k]
        gap = lambda i: [(r[i] - r[5]) / r[5] * 100 for r in rs]
        impr = [(r[2] - r[5]) / r[2] * 100 for r in rs]
        summary.append([k, len(rs), round(st.mean(impr), 2), round(st.mean(gap(3)), 2),
                        round(max(gap(3)), 2), round(st.mean(gap(4)), 2), round(max(gap(4)), 2),
                        sum(1 for x in gap(4) if x < 1e-6), round(st.mean(r[6] + r[7] for r in rs), 3),
                        round(st.mean(r[8] for r in rs), 2)])
    write_csv("experiment_summary.csv",
              ["k_stops", "n_instances", "hk_vs_input_savings_pct", "nn_gap_mean_pct", "nn_gap_max_pct",
               "nn2opt_gap_mean_pct", "nn2opt_gap_max_pct", "nn2opt_optimal_count", "ms_heuristic_total",
               "ms_heldkarp"], summary)
    return rows, summary


def exp_scaling():
    """Waktu vs ukuran input: HK (eksponensial), NN+2opt (polinomial), Dijkstra (V log V)."""
    rows = []
    rng = random.Random(5)
    for k in range(6, 17):  # Held-Karp
        pts = [(rng.random() * 50, rng.random() * 50) for _ in range(k + 1)]
        d = [[math.dist(a, b) for b in pts] for a in pts]
        _, t = timed(held_karp, d)
        rows.append(["held_karp", k, round(t * 1e3, 2)])
    for n in (25, 50, 100, 200, 300, 400):  # NN + 2-opt
        pts = [(rng.random() * 100, rng.random() * 100) for _ in range(n + 1)]
        d = [[math.dist(a, b) for b in pts] for a in pts]
        nn, t1 = timed(nearest_neighbor, d)
        (_, stats), t2 = timed(lambda: two_opt(d, nn))
        rows.append(["nn", n, round(t1 * 1e3, 2)])
        rows.append(["nn+2opt", n, round((t1 + t2) * 1e3, 2)])
    for v in (200, 800, 3200, 12800, 51200):  # Dijkstra pada graf acak E=3V
        g = Graph()
        for i in range(v):
            g.add_node(i)
        for i in range(1, v):
            g.add_edge(i, rng.randrange(i), rng.uniform(1, 10))
        for _ in range(2 * v):
            a, b = rng.sample(range(v), 2)
            g.add_edge(a, b, rng.uniform(1, 10))
        _, t = timed(dijkstra, g, 0, repeat=3)
        rows.append(["dijkstra", v, round(t * 1e3, 2)])
    write_csv("experiment_scaling.csv", ["algoritma", "ukuran", "ms"], rows)
    return rows


def exp_scenarios(g, sc):
    rows = []
    for name, (depot, stops) in sc.items():
        row = [name, len(stops)]
        for m in ("input", "nn", "nn2opt", "held_karp"):
            if m == "held_karp" and len(stops) > 15:
                row += ["-", "-"]
                continue
            r = solve(g, depot, stops, m)
            row += [round(r.cost_km, 3), round(r.runtime_s * 1e3, 2)]
        rows.append(row)
    write_csv("experiment_scenarios.csv",
              ["scenario", "n_stops", "km_input", "ms_input", "km_nn", "ms_nn", "km_nn2opt", "ms_nn2opt",
               "km_heldkarp", "ms_heldkarp"], rows)
    return rows


def make_figures(g, summary, scaling, sc):
    ks = [s[0] for s in summary]
    fig, ax = plt.subplots(figsize=(6.4, 4))
    ax.plot(ks, [s[3] for s in summary], "o-", label="NN (rata-rata)")
    ax.plot(ks, [s[5] for s in summary], "s-", label="NN + 2-opt (rata-rata)")
    ax.plot(ks, [s[6] for s in summary], "s--", alpha=0.5, label="NN + 2-opt (maks)")
    ax.set_xlabel("Jumlah titik antar")
    ax.set_ylabel("Selisih terhadap optimum (%)")
    ax.set_title("Kualitas solusi heuristik vs Held-Karp")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "gap_vs_k.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 4))
    hk = [(r[1], r[2]) for r in scaling if r[0] == "held_karp"]
    ax.semilogy(*zip(*hk), "o-", label="Held-Karp  O(n² 2ⁿ)")
    for name, mk in (("nn+2opt", "s-"), ("nn", "^-")):
        pts = [(r[1], r[2]) for r in scaling if r[0] == name]
        ax.semilogy(*zip(*pts), mk, label=name.upper().replace("+", " + "))
    ax.set_xlabel("Jumlah titik antar")
    ax.set_ylabel("Waktu (ms, skala log)")
    ax.set_title("Pengaruh ukuran input terhadap waktu")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG / "waktu_vs_ukuran.png", dpi=160)
    plt.close(fig)

    for name, method in (("S2", "held_karp"), ("S4", "nn2opt")):
        depot, stops = sc[name]
        r = solve(g, depot, stops, method)
        plot_route(g, r, str(FIG / f"rute_{name}.png"),
                   title=f"Skenario {name} - {method}: {r.cost_km:.1f} km, {len(stops)} titik")


def write_report(summary, scaling, scen_rows):
    L = ["# Ringkasan eksperimen (dihasilkan otomatis oleh scripts/run_experiments.py)", "",
         "## A. Perbandingan pada submasalah sama (TSP), instans acak dari 41 lokasi Jakarta", "",
         "| k | n | Hemat HK vs urutan input (%) | NN gap rata2 (%) | NN gap maks (%) | 2-opt gap rata2 (%) | 2-opt gap maks (%) | 2-opt optimal | ms heuristik | ms Held-Karp |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    L += ["| " + " | ".join(str(x) for x in s) + " |" for s in summary]
    L += ["", "## B. Skalabilitas (ms)", "", "| algoritma | ukuran | ms |", "|---|---|---|"]
    L += [f"| {a} | {n} | {m} |" for a, n, m in scaling]
    L += ["", "## C. Skenario S1-S5 (km, ms)", "",
          "| skenario | titik | input km | input ms | NN km | NN ms | 2-opt km | 2-opt ms | HK km | HK ms |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    L += ["| " + " | ".join(str(x) for x in r) + " |" for r in scen_rows]
    (OUT / "experiment_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    graph = load_graph(ROOT / "data" / "nodes.csv", ROOT / "data" / "edges.csv")
    scen = load_scenarios(ROOT / "data" / "scenarios.csv")
    _, summ = exp_comparison(graph)
    print("A selesai")
    scal = exp_scaling()
    print("B selesai")
    srows = exp_scenarios(graph, scen)
    print("C selesai")
    make_figures(graph, summ, scal, scen)
    write_report(summ, scal, srows)
    print("laporan: outputs/experiment_report.md")
