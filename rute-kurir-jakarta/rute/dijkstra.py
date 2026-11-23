"""Algoritma 1 - Dijkstra (binary heap). Implementasi sendiri; hanya memakai heapq dari stdlib."""
from __future__ import annotations

import heapq

from .graph import Graph

INF = float("inf")


def dijkstra(graph: Graph, src: int, trace: list[str] | None = None):
    """Jarak terpendek dari src ke semua simpul.

    Return (dist, prev). dist[v] = INF bila v tidak terjangkau.
    Kompleksitas waktu O((V+E) log V), ruang O(V+E).
    """
    dist = {v: INF for v in graph.adj}
    prev: dict[int, int] = {}
    dist[src] = 0.0
    pq = [(0.0, src)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > dist[u]:  # entri usang di heap
            continue
        if trace is not None:
            trace.append(f"POP  {graph.names[u]} (d={du:.3f})")
        for v, w in graph.adj[u]:
            nd = du + w
            if nd < dist[v]:
                if trace is not None:
                    old = "inf" if dist[v] == INF else f"{dist[v]:.3f}"
                    trace.append(f"  relax {graph.names[v]}: {old} -> {nd:.3f}")
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev


def reconstruct_path(prev: dict[int, int], src: int, dst: int) -> list[int]:
    """Susun jalur src -> dst dari peta predecessor."""
    path = [dst]
    while path[-1] != src:
        path.append(prev[path[-1]])
    path.reverse()
    return path
