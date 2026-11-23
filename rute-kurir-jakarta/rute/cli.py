"""CLI: python -m rute.cli --scenario S2 --method auto [--plot outputs/figures/rute.png]"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from .graph import load_graph
from .tsp import solve

ROOT = Path(__file__).resolve().parents[1]


def load_scenarios(path: Path) -> dict[str, tuple[int, list[int]]]:
    out = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["scenario"]] = (int(row["depot"]), [int(x) for x in row["stops"].split(";") if x])
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Optimasi rute kurir Jakarta")
    p.add_argument("--data", default=str(ROOT / "data"), help="folder berisi nodes.csv, edges.csv, scenarios.csv")
    p.add_argument("--scenario", help="nama skenario (S1..S5)")
    p.add_argument("--depot", type=int, default=0)
    p.add_argument("--stops", help="daftar id titik antar dipisah koma, mis. 3,8,15 (mengganti --scenario)")
    p.add_argument("--method", default="auto", choices=["auto", "held_karp", "nn", "nn2opt", "input", "brute"])
    p.add_argument("--plot", help="simpan peta rute ke berkas PNG (butuh matplotlib)")
    a = p.parse_args(argv)

    data = Path(a.data)
    g = load_graph(data / "nodes.csv", data / "edges.csv")
    if a.stops:
        depot, stops = a.depot, [int(x) for x in a.stops.split(",") if x.strip()]
    elif a.scenario:
        sc = load_scenarios(data / "scenarios.csv")
        if a.scenario not in sc:
            print(f"Skenario tidak ada. Pilihan: {', '.join(sc)}", file=sys.stderr)
            return 2
        depot, stops = sc[a.scenario]
    else:
        print("Isi --scenario atau --stops", file=sys.stderr)
        return 2

    try:
        r = solve(g, depot, stops, a.method)
    except ValueError as e:
        print(f"Input tidak valid: {e}", file=sys.stderr)
        return 2

    print(f"Metode      : {r.method}")
    print(f"Jumlah titik: {len(r.order) - 1}")
    print(f"Total jarak : {r.cost_km:.3f} km  (waktu hitung {r.runtime_s * 1000:.1f} ms)")
    print("Urutan      : " + " -> ".join(g.names[v] for v in r.order) + f" -> {g.names[r.order[0]]}")
    if r.extra:
        print(f"Info        : {r.extra}")
    if a.plot:
        from .viz import plot_route

        plot_route(g, r, a.plot)
        print(f"Peta disimpan: {a.plot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
