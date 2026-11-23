"""Hasilkan trace langkah kerja ketiga algoritma ke outputs/trace/*.txt (D06)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rute.cli import load_scenarios  # noqa: E402
from rute.dijkstra import dijkstra  # noqa: E402
from rute.graph import Graph, load_graph  # noqa: E402
from rute.tsp import build_matrix, held_karp, nearest_neighbor, tour_cost, two_opt  # noqa: E402

OUT = ROOT / "outputs" / "trace"
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, lines: list[str]) -> None:
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"ditulis {name} ({len(lines)} baris)")


def trace_dijkstra_kecil() -> None:
    g = Graph()
    for i, n in enumerate("ABCD"):
        g.add_node(i, n)
    for u, v, w in [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)]:
        g.add_edge(u, v, w)
    tr: list[str] = []
    dist, _ = dijkstra(g, 0, trace=tr)
    lines = ["# Trace Dijkstra - graf contoh 4 simpul (bisa diverifikasi dengan tangan)",
             "# Sisi: A-B=4, A-C=1, C-B=2, B-D=1, C-D=5 ; sumber = A", ""]
    lines += tr
    lines += ["", "Hasil akhir: " + ", ".join(f"{g.names[k]}={v:g}" for k, v in dist.items())]
    write("dijkstra_graf_kecil.txt", lines)


def trace_dijkstra_jakarta(g) -> None:
    tr: list[str] = []
    dijkstra(g, 0, trace=tr)
    lines = ["# Trace Dijkstra dari Depo Kemayoran pada graf Jakarta (28 baris pertama)", ""] + tr[:28]
    write("dijkstra_jakarta.txt", lines)


def trace_held_karp(g, sc) -> None:
    depot, stops = sc["S1"]
    stops = stops[:4]
    nodes = [depot] + stops
    d, _ = build_matrix(g, nodes)
    lines = ["# Trace Held-Karp - depo + 4 titik antar dari skenario S1",
             "# Indeks lokal: 0=depo, " + ", ".join(f"{i + 1}={g.names[s]}" for i, s in enumerate(stops)), "",
             "Matriks jarak terpendek (km):"]
    for row in d:
        lines.append("  " + " ".join(f"{x:7.2f}" for x in row))
    lines += ["", "Pembaruan tabel DP (hanya saat nilai membaik):"]
    tr: list[str] = []
    cost, tour = held_karp(d, trace=tr)
    lines += ["  " + t for t in tr]
    lines += ["", f"Tur optimum (indeks lokal): {tour} + kembali ke 0",
              f"Biaya optimum: {cost:.3f} km",
              "Nama: " + " -> ".join(g.names[nodes[i]] for i in tour) + f" -> {g.names[nodes[0]]}"]
    write("held_karp_4_titik.txt", lines)


def trace_two_opt(g, sc) -> None:
    depot, stops = sc["S4"]
    nodes = [depot] + stops
    d, _ = build_matrix(g, nodes)
    nn = nearest_neighbor(d)
    lines = ["# Trace Nearest Neighbor + 2-opt - skenario S4 (25 titik antar)", "",
             f"Tur NN (indeks lokal): {nn}", f"Biaya NN: {tour_cost(d, nn):.3f} km", "", "Langkah 2-opt:"]
    tr: list[str] = []
    t2, st = two_opt(d, nn, trace=tr)
    lines += ["  " + t for t in tr]
    lines += ["", f"Tur akhir: {t2}", f"Biaya akhir: {tour_cost(d, t2):.3f} km",
              f"Pass: {st['passes']} | Pertukaran: {st['swaps']}"]
    write("nn_2opt_S4.txt", lines)


if __name__ == "__main__":
    graph = load_graph(ROOT / "data" / "nodes.csv", ROOT / "data" / "edges.csv")
    scen = load_scenarios(ROOT / "data" / "scenarios.csv")
    trace_dijkstra_kecil()
    trace_dijkstra_jakarta(graph)
    trace_held_karp(graph, scen)
    trace_two_opt(graph, scen)
