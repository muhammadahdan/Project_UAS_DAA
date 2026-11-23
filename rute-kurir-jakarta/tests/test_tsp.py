import math
import random

import pytest

from rute.graph import Graph
from rute.tsp import brute_force, held_karp, nearest_neighbor, solve, tour_cost, two_opt

from conftest import random_graph


def rand_matrix(n, seed):
    rng = random.Random(seed)
    pts = [(rng.random() * 50, rng.random() * 50) for _ in range(n)]
    return [[math.dist(a, b) for b in pts] for a in pts]


def is_perm(tour, n):
    return sorted(tour) == list(range(n)) and tour[0] == 0


# ---------------------------------------------------------------- normal
def test_TC07_held_karp_contoh_manual_4_titik():
    """Normal: persegi 1x1 -> tur optimum = 4.0."""
    pts = [(0, 0), (1, 0), (1, 1), (0, 1)]
    d = [[math.dist(a, b) for b in pts] for a in pts]
    cost, tour = held_karp(d)
    assert math.isclose(cost, 4.0) and is_perm(tour, 4)


@pytest.mark.parametrize("seed", range(8))
def test_TC08_held_karp_sama_dengan_brute_force(seed):
    """Normal: 8 instans acak (7 titik antar) - biaya HK == brute force."""
    d = rand_matrix(8, seed)
    assert math.isclose(held_karp(d)[0], brute_force(d)[0], abs_tol=1e-9)


@pytest.mark.parametrize("seed", range(8))
def test_TC09_two_opt_valid_dan_tidak_lebih_buruk_dari_nn(seed):
    """Normal: 2-opt menghasilkan permutasi valid, biaya <= NN, >= optimum."""
    d = rand_matrix(11, seed)
    nn = nearest_neighbor(d)
    t2, _ = two_opt(d, nn)
    opt, _ = held_karp(d)
    assert is_perm(nn, 11) and is_perm(t2, 11)
    assert tour_cost(d, t2) <= tour_cost(d, nn) + 1e-9
    assert tour_cost(d, t2) >= opt - 1e-9


def test_TC10_solve_biaya_sama_dengan_hitung_ulang(jakarta):
    """Normal: biaya Route = jumlah panjang ruas pada road_path."""
    r = solve(jakarta, 0, [3, 8, 15, 22, 30, 36], "held_karp")
    w = {}
    for u, nb in jakarta.adj.items():
        for v, c in nb:
            w[(u, v)] = min(w.get((u, v), 1e18), c)
    total = sum(w[(a, b)] for a, b in zip(r.road_path, r.road_path[1:]))
    assert math.isclose(total, r.cost_km, abs_tol=1e-6)
    assert r.road_path[0] == r.road_path[-1] == 0


def test_TC11_held_karp_tidak_lebih_buruk_dari_urutan_input(jakarta):
    """Normal: optimum <= baseline urutan masukan."""
    stops = [25, 4, 41, 12, 33, 7]
    assert solve(jakarta, 0, stops, "held_karp").cost_km <= solve(jakarta, 0, stops, "input").cost_km + 1e-9


# ---------------------------------------------------------------- batas
def test_TC12_nol_titik_antar(jakarta):
    """Batas: daftar kosong -> rute hanya depo, biaya 0."""
    r = solve(jakarta, 0, [], "held_karp")
    assert r.cost_km == 0.0 and r.order == [0]


def test_TC13_satu_titik_antar(jakarta):
    """Batas: 1 titik -> pergi-pulang = 2x jarak terpendek."""
    r = solve(jakarta, 0, [15], "held_karp")
    r2 = solve(jakarta, 0, [15], "nn2opt")
    assert r.order == [0, 15] and math.isclose(r.cost_km, r2.cost_km)


def test_TC14_dua_titik_antar(jakarta):
    """Batas: 2 titik -> HK == brute force == nn2opt."""
    costs = {m: solve(jakarta, 0, [15, 3], m).cost_km for m in ("held_karp", "brute", "nn2opt")}
    assert len({round(c, 6) for c in costs.values()}) == 1


def test_TC15_semua_lokasi_dikunjungi(jakarta):
    """Batas: 41 titik (maksimum graf) dengan nn2opt - setiap lokasi tepat sekali."""
    r = solve(jakarta, 0, list(range(1, 42)), "nn2opt")
    assert sorted(r.order) == list(range(42))


# ------------------------------------------------------------ tidak valid
def test_TC16_titik_duplikat_diabaikan(jakarta):
    """Tidak valid: duplikat dibuang; hasil sama dengan tanpa duplikat."""
    a = solve(jakarta, 0, [3, 8, 3, 15, 8], "held_karp")
    b = solve(jakarta, 0, [3, 8, 15], "held_karp")
    assert sorted(a.order) == sorted(b.order) and math.isclose(a.cost_km, b.cost_km)


def test_TC17_depo_di_dalam_daftar_titik_diabaikan(jakarta):
    """Tidak valid: depo muncul sebagai titik antar -> dibuang, depo hanya sekali."""
    r = solve(jakarta, 0, [0, 3, 8], "held_karp")
    assert r.order.count(0) == 1 and sorted(r.order) == [0, 3, 8]


def test_TC18_id_tidak_dikenal_ditolak(jakarta):
    """Tidak valid: id titik tidak ada -> ValueError yang jelas (bukan KeyError)."""
    with pytest.raises(ValueError, match="tidak dikenal"):
        solve(jakarta, 0, [3, 999], "held_karp")


def test_TC19_titik_tak_terjangkau_ditolak():
    """Tidak valid: titik terisolasi -> ValueError, bukan hasil diam-diam salah."""
    g = random_graph(8, 4, 1)
    g.add_node(99, "terisolasi")
    with pytest.raises(ValueError, match="tidak terjangkau"):
        solve(g, 0, [1, 2, 99], "held_karp")


def test_TC20_metode_tidak_dikenal(jakarta):
    with pytest.raises(ValueError):
        solve(jakarta, 0, [3], "ajaib")
