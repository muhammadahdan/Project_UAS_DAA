"""Struktur data graf jalan (tidak berarah, berbobot jarak km). Dikembangkan sendiri."""
from __future__ import annotations

import csv
import math
from pathlib import Path


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Jarak garis lurus di permukaan bumi (km)."""
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


class Graph:
    """Graf tidak berarah dengan adjacency list: adj[u] = [(v, bobot_km), ...]."""

    def __init__(self) -> None:
        self.names: dict[int, str] = {}
        self.coords: dict[int, tuple[float, float]] = {}
        self.adj: dict[int, list[tuple[int, float]]] = {}

    @property
    def nodes(self) -> list[int]:
        return list(self.adj)

    def add_node(self, nid: int, name: str = "", lat: float = 0.0, lon: float = 0.0) -> None:
        self.names[nid] = name or str(nid)
        self.coords[nid] = (lat, lon)
        self.adj.setdefault(nid, [])

    def add_edge(self, u: int, v: int, w: float) -> None:
        if w < 0:
            raise ValueError("Bobot negatif tidak didukung Dijkstra")
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    def edge_count(self) -> int:
        return sum(len(v) for v in self.adj.values()) // 2


def load_graph(nodes_csv: str | Path, edges_csv: str | Path) -> Graph:
    g = Graph()
    with open(nodes_csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g.add_node(int(row["id"]), row["name"], float(row["lat"]), float(row["lon"]))
    with open(edges_csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g.add_edge(int(row["u"]), int(row["v"]), float(row["km"]))
    return g
