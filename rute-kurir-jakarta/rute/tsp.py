"""Algoritma 2 (Held-Karp), Algoritma 3 (Nearest Neighbor + 2-opt), dan solver gabungan.

Matriks jarak d (n x n) memakai indeks lokal: 0 = depo, 1..n-1 = titik antar.
"""
from __future__ import annotations

import itertools
import time
from dataclasses import dataclass, field

from .dijkstra import INF, dijkstra, reconstruct_path
from .graph import Graph


def build_matrix(graph: Graph, nodes: list[int]):
    """Matriks jarak terpendek antar `nodes` lewat Dijkstra (satu run per simpul)."""
    n = len(nodes)
    d = [[0.0] * n for _ in range(n)]
    prevs = []
    for i, s in enumerate(nodes):
        dist, prev = dijkstra(graph, s)
        prevs.append(prev)
        for j, t in enumerate(nodes):
            d[i][j] = dist[t]
    return d, prevs


def tour_cost(d: list[list[float]], tour: list[int]) -> float:
    """Biaya tur tertutup (kembali ke tour[0])."""
    n = len(tour)
    return sum(d[tour[i]][tour[(i + 1) % n]] for i in range(n))


# ---------------------------------------------------------------- Held-Karp
def held_karp(d: list[list[float]], trace: list[str] | None = None):
    """TSP eksak dengan DP bitmask. Waktu O(n^2 2^n), ruang O(n 2^n)."""
    n = len(d)
    m = n - 1  # jumlah titik antar; titik k (1..m) -> bit k-1
    if m == 0:  # perbaikan BUG-1: tidak ada titik antar
        return 0.0, [0]
    size = 1 << m
    dp = [[INF] * m for _ in range(size)]
    par = [[-1] * m for _ in range(size)]
    for j in range(m):
        dp[1 << j][j] = d[0][j + 1]
    for mask in range(1, size):
        row = dp[mask]
        for last in range(m):
            cur = row[last]
            if cur == INF:
                continue
            dl = d[last + 1]
            for nxt in range(m):
                bit = 1 << nxt
                if mask & bit:
                    continue
                c = cur + dl[nxt + 1]
                nm = mask | bit
                if c < dp[nm][nxt]:
                    dp[nm][nxt] = c
                    par[nm][nxt] = last
                    if trace is not None:
                        s = "{" + ",".join(str(k + 1) for k in range(m) if nm >> k & 1) + "}"
                        trace.append(f"dp[{s}, akhir={nxt + 1}] = {c:.3f}  (dari akhir={last + 1})")
    full = size - 1
    best, bl = min((dp[full][l] + d[l + 1][0], l) for l in range(m))
    tour: list[int] = []
    mask, l = full, bl
    while l != -1:
        tour.append(l + 1)
        pl = par[mask][l]
        mask ^= 1 << l
        l = pl
    tour.reverse()
    return best, [0] + tour


# ------------------------------------------------------ Nearest Neighbor + 2-opt
def nearest_neighbor(d: list[list[float]], start: int = 0) -> list[int]:
    n = len(d)
    seen = {start}
    tour = [start]
    while len(tour) < n:
        cur = tour[-1]
        nxt = min((j for j in range(n) if j not in seen), key=lambda j: d[cur][j])
        tour.append(nxt)
        seen.add(nxt)
    return tour


def two_opt(d, tour, eps: float = 1e-9, max_passes: int = 1000, trace: list[str] | None = None):
    """Perbaikan lokal 2-opt (first-improvement). Posisi 0 (depo) tidak pernah dibalik."""
    tour = tour[:]
    n = len(tour)
    passes = swaps = 0
    improved = True
    while improved and passes < max_passes:
        improved = False
        passes += 1
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                a, b = tour[i - 1], tour[i]
                c, e = tour[j], tour[(j + 1) % n]
                delta = d[a][c] + d[b][e] - d[a][b] - d[c][e]
                if delta < -eps:
                    if trace is not None:
                        trace.append(
                            f"pass {passes}: balik segmen posisi {i}..{j} "
                            f"(ganti sisi {a}-{b} & {c}-{e} -> {a}-{c} & {b}-{e}), delta={delta:.3f}"
                        )
                    tour[i : j + 1] = reversed(tour[i : j + 1])
                    swaps += 1
                    improved = True
    return tour, {"passes": passes, "swaps": swaps}


def brute_force(d):
    """Pembanding untuk verifikasi (n kecil): coba semua permutasi."""
    n = len(d)
    best, best_t = INF, None
    for perm in itertools.permutations(range(1, n)):
        t = [0, *perm]
        c = tour_cost(d, t)
        if c < best:
            best, best_t = c, t
    return best, best_t


# ------------------------------------------------------------------ Solver
@dataclass
class Route:
    method: str
    order: list[int]          # id simpul graf: depo + urutan kunjungan (tanpa pengulangan depo)
    cost_km: float
    road_path: list[int]      # jalur lengkap menyusuri ruas jalan, depo -> ... -> depo
    runtime_s: float
    extra: dict = field(default_factory=dict)


def expand_road_path(prevs, nodes, tour):
    full: list[int] = [nodes[tour[0]]]
    n = len(tour)
    for k in range(n):
        i, j = tour[k], tour[(k + 1) % n]
        seg = reconstruct_path(prevs[i], nodes[i], nodes[j])
        full.extend(seg[1:])
    return full


def validate_stops(graph: Graph, depot: int, stops: list[int]) -> list[int]:
    """Bersihkan & periksa masukan. Perbaikan BUG-2, BUG-3, BUG-4.

    - id tidak ada di graf        -> ValueError
    - duplikat / depo dalam daftar -> dibuang (urutan pertama dipertahankan)
    """
    if depot not in graph.adj:
        raise ValueError(f"depo {depot} tidak dikenal di graf")
    clean: list[int] = []
    seen = {depot}
    for s in stops:
        if s not in graph.adj:
            raise ValueError(f"titik {s} tidak dikenal di graf")
        if s not in seen:
            seen.add(s)
            clean.append(s)
    return clean


def solve(graph: Graph, depot: int, stops: list[int], method: str = "auto", hk_limit: int = 15) -> Route:
    t0 = time.perf_counter()
    stops = validate_stops(graph, depot, stops)
    nodes = [depot] + stops
    d, prevs = build_matrix(graph, nodes)
    for j in range(1, len(nodes)):  # BUG-4: jangan diam-diam menghasilkan biaya inf
        if d[0][j] == INF:
            raise ValueError(f"titik {nodes[j]} tidak terjangkau dari depo {depot}")
    extra: dict = {}
    if method == "auto":
        method = "held_karp" if len(stops) <= hk_limit else "nn2opt"
    if method == "held_karp":
        cost, tour = held_karp(d)
    elif method == "brute":
        cost, tour = brute_force(d)
    elif method == "nn":
        tour = nearest_neighbor(d)
        cost = tour_cost(d, tour)
    elif method == "nn2opt":
        tour = nearest_neighbor(d)
        extra["nn_cost"] = tour_cost(d, tour)
        tour, stats = two_opt(d, tour)
        extra.update(stats)
        cost = tour_cost(d, tour)
    elif method == "input":
        tour = list(range(len(nodes)))
        cost = tour_cost(d, tour)
    else:
        raise ValueError(f"metode tidak dikenal: {method}")
    road = expand_road_path(prevs, nodes, tour)
    return Route(method, [nodes[i] for i in tour], cost, road, time.perf_counter() - t0, extra)
