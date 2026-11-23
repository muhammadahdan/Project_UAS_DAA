import random
from pathlib import Path

import pytest

from rute.graph import Graph, load_graph

DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="session")
def jakarta():
    return load_graph(DATA / "nodes.csv", DATA / "edges.csv")


def random_graph(n: int, extra: int, seed: int) -> Graph:
    """Graf acak terhubung (pohon acak + sisi tambahan) untuk uji silang."""
    rng = random.Random(seed)
    g = Graph()
    for i in range(n):
        g.add_node(i, f"n{i}")
    for i in range(1, n):
        g.add_edge(i, rng.randrange(i), round(rng.uniform(1, 10), 2))
    for _ in range(extra):
        a, b = rng.sample(range(n), 2)
        g.add_edge(a, b, round(rng.uniform(1, 10), 2))
    return g


def floyd_warshall(g: Graph):
    """Referensi independen untuk memverifikasi Dijkstra."""
    nodes = g.nodes
    inf = float("inf")
    d = {u: {v: (0.0 if u == v else inf) for v in nodes} for u in nodes}
    for u in nodes:
        for v, w in g.adj[u]:
            d[u][v] = min(d[u][v], w)
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d
