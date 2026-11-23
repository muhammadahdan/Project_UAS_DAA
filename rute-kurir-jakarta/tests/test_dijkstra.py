import math

import pytest

from rute.dijkstra import dijkstra, reconstruct_path
from rute.graph import Graph

from conftest import floyd_warshall, random_graph


def small():
    g = Graph()
    for i, n in enumerate("ABCDE"):
        g.add_node(i, n)
    for u, v, w in [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5)]:
        g.add_edge(u, v, w)
    return g  # E (4) terisolasi


def test_TC01_dijkstra_contoh_manual():
    """Normal: hasil dihitung tangan A->B=3 (via C), A->D=4."""
    dist, prev = dijkstra(small(), 0)
    assert dist[1] == 3 and dist[2] == 1 and dist[3] == 4
    assert reconstruct_path(prev, 0, 3) == [0, 2, 1, 3]


@pytest.mark.parametrize("seed", range(5))
def test_TC02_dijkstra_sama_dengan_floyd_warshall(seed):
    """Normal: 5 graf acak, semua pasangan sama dengan Floyd-Warshall."""
    g = random_graph(25, 30, seed)
    ref = floyd_warshall(g)
    for s in g.nodes:
        dist, _ = dijkstra(g, s)
        for t in g.nodes:
            assert math.isclose(dist[t], ref[s][t], abs_tol=1e-9)


def test_TC03_dijkstra_sumber_sama_dengan_tujuan():
    """Batas: jarak ke diri sendiri = 0."""
    dist, _ = dijkstra(small(), 2)
    assert dist[2] == 0.0


def test_TC04_dijkstra_simpul_terisolasi_tak_terjangkau():
    """Batas: simpul tak terhubung -> inf."""
    dist, _ = dijkstra(small(), 0)
    assert dist[4] == float("inf")


def test_TC05_bobot_negatif_ditolak():
    """Tidak valid: bobot negatif."""
    g = Graph()
    g.add_node(0)
    g.add_node(1)
    with pytest.raises(ValueError):
        g.add_edge(0, 1, -1.0)


def test_TC06_graf_jakarta_terhubung(jakarta):
    """Data: seluruh 42 lokasi terjangkau dari depo."""
    dist, _ = dijkstra(jakarta, 0)
    assert all(v < float("inf") for v in dist.values())
    assert len(dist) == 42
