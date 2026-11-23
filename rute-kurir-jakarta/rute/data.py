"""Dataset sintetis: 42 lokasi di Jakarta + ruas jalan sintetis + skenario pengantaran.

Koordinat = perkiraan titik pusat kawasan (informasi geografis publik, BUKAN alamat pribadi).
Ruas jalan = sintetis: k tetangga terdekat, jarak = garis lurus x faktor kelokan acak (1.2-1.6).
Tidak ada data pribadi/rahasia. Semua deterministik lewat seed.
"""
from __future__ import annotations

import random

from .graph import haversine_km

# (id, nama, lat, lon)  id 0 = depo
LOCATIONS = [
    (0, "Depo Kemayoran", -6.1650, 106.8500),
    (1, "Monas", -6.1754, 106.8272),
    (2, "Kota Tua", -6.1352, 106.8133),
    (3, "Kelapa Gading", -6.1587, 106.9055),
    (4, "Sunter", -6.1393, 106.8696),
    (5, "Cempaka Putih", -6.1760, 106.8700),
    (6, "Senen", -6.1760, 106.8450),
    (7, "Menteng", -6.1950, 106.8330),
    (8, "Tanah Abang", -6.1860, 106.8110),
    (9, "Grogol", -6.1670, 106.7890),
    (10, "Kebon Jeruk", -6.1900, 106.7700),
    (11, "Kembangan", -6.1880, 106.7370),
    (12, "Slipi", -6.2000, 106.7960),
    (13, "Kuningan", -6.2300, 106.8300),
    (14, "SCBD", -6.2250, 106.8100),
    (15, "Blok M", -6.2440, 106.7990),
    (16, "Kebayoran Lama", -6.2400, 106.7750),
    (17, "Pondok Indah", -6.2650, 106.7840),
    (18, "Cilandak", -6.2900, 106.7980),
    (19, "Pasar Minggu", -6.2840, 106.8450),
    (20, "Tebet", -6.2260, 106.8540),
    (21, "Cawang", -6.2430, 106.8680),
    (22, "Jatinegara", -6.2150, 106.8700),
    (23, "Pulogadung", -6.1850, 106.9080),
    (24, "Rawamangun", -6.1970, 106.8900),
    (25, "Cakung", -6.1800, 106.9400),
    (26, "Kramat Jati", -6.2700, 106.8660),
    (27, "Pasar Rebo", -6.3200, 106.8700),
    (28, "Ciracas", -6.3270, 106.8820),
    (29, "Duren Sawit", -6.2330, 106.9100),
    (30, "Pluit", -6.1180, 106.7900),
    (31, "PIK", -6.1070, 106.7400),
    (32, "Cengkareng", -6.1500, 106.7300),
    (33, "Kalideres", -6.1550, 106.7000),
    (34, "Tanjung Priok", -6.1090, 106.8800),
    (35, "Ancol", -6.1250, 106.8420),
    (36, "Mangga Dua", -6.1380, 106.8300),
    (37, "Cikini", -6.1900, 106.8400),
    (38, "Manggarai", -6.2100, 106.8500),
    (39, "Pancoran", -6.2430, 106.8450),
    (40, "Lebak Bulus", -6.2890, 106.7740),
    (41, "Ragunan", -6.3100, 106.8200),
]

SCENARIO_SIZES = {"S1": 6, "S2": 10, "S3": 13, "S4": 25, "S5": 41}


def build_edges(k: int = 3, seed: int = 42):
    """Ruas jalan sintetis: tiap simpul ke k tetangga terdekat + penyambung komponen."""
    rng = random.Random(seed)
    n = len(LOCATIONS)
    hav = lambda a, b: haversine_km(LOCATIONS[a][2], LOCATIONS[a][3], LOCATIONS[b][2], LOCATIONS[b][3])
    pairs: set[tuple[int, int]] = set()
    for i in range(n):
        near = sorted((j for j in range(n) if j != i), key=lambda j: hav(i, j))[:k]
        for j in near:
            pairs.add((min(i, j), max(i, j)))
    # union-find agar graf terhubung
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in pairs:
        parent[find(a)] = find(b)
    while len({find(i) for i in range(n)}) > 1:
        best = min(
            ((hav(a, b), a, b) for a in range(n) for b in range(a + 1, n) if find(a) != find(b)),
        )
        _, a, b = best
        pairs.add((a, b))
        parent[find(a)] = find(b)
    return [(a, b, round(hav(a, b) * rng.uniform(1.2, 1.6), 3)) for a, b in sorted(pairs)]


def build_scenarios(seed: int = 7):
    """Skenario: depo = 0; titik antar dipilih acak (seed tetap)."""
    rng = random.Random(seed)
    out = {}
    for name, size in SCENARIO_SIZES.items():
        out[name] = sorted(rng.sample(range(1, len(LOCATIONS)), size))
    return out
