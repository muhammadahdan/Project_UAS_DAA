# D06 – Trace Algoritma dan Analisis Kompleksitas

Seluruh trace dihasilkan oleh kode (`python scripts/make_traces.py` → `outputs/trace/`), bukan ditulis tangan, sehingga bisa direproduksi.

## 1. Trace Dijkstra (graf 4 simpul, dapat dicek dengan tangan)

Sisi: A–B = 4, A–C = 1, C–B = 2, B–D = 1, C–D = 5. Sumber A.

```
POP  A (d=0.000)
  relax B: inf -> 4.000
  relax C: inf -> 1.000
POP  C (d=1.000)
  relax B: 4.000 -> 3.000      <- jalur A-C-B (3) mengalahkan A-B langsung (4)
  relax D: inf -> 6.000
POP  B (d=3.000)
  relax D: 6.000 -> 4.000      <- jalur A-C-B-D (4) mengalahkan A-C-D (6)
POP  D (d=4.000)
Hasil: A=0, B=3, C=1, D=4
```

Keputusan algoritma: simpul dengan jarak sementara terkecil selalu "dikunci" lebih dulu; nilai sementara diperbaiki ketika ditemukan jalur lewat simpul yang baru dikunci. Trace pada graf Jakarta ada di `outputs/trace/dijkstra_jakarta.txt`.

## 2. Trace Held-Karp (depo + 4 titik antar dari S1)

Indeks lokal: 0 = Depo Kemayoran, 1 = Sunter, 2 = Cempaka Putih, 3 = Kebon Jeruk, 4 = Cawang.

Matriks jarak terpendek (km) hasil Dijkstra:

```
   0.00    4.34    3.31   14.41   13.48
   4.34    0.00    7.65   18.75   17.82
   3.31    7.65    0.00   17.48   14.48
  14.41   18.75   17.48    0.00   19.42
  13.48   17.82   14.48   19.42    0.00
```

Cuplikan pembaruan tabel DP (selengkapnya di `outputs/trace/held_karp_4_titik.txt`):

```
dp[{1,2}, akhir=2] = 11.988  (dari akhir=1)      # 0->1->2: 4.34 + 7.65 = 11.99
dp[{1,2}, akhir=1] = 10.959  (dari akhir=2)      # 0->2->1: 3.31 + 7.65 = 10.96
...
dp[{1,2,3,4}, akhir=1] = 55.954  (dari akhir=2)  # nilai akhir terbaik sebelum pulang
```

Hasil: tur optimum **0 → 3 → 4 → 2 → 1 → 0**, biaya 60,293 km.
Verifikasi tangan: 14,41 + 19,42 + 14,48 + 7,65 + 4,34 = **60,30** ✓ (selisih pembulatan).

Perubahan keadaan yang bisa ditelusuri: setiap baris adalah satu sel DP `dp[S, j]` yang membaik, beserta predecessor-nya; rekonstruksi mengikuti predecessor mundur dari akhir terbaik.

## 3. Trace Nearest Neighbor + 2-opt (S4, 25 titik antar)

```
Biaya NN: 165.087 km
pass 1: balik segmen posisi 15..23 (ganti sisi 4-13 & 9-15 -> 4-9 & 13-15), delta=-2.611
pass 1: balik segmen posisi 18..20 (ganti sisi 11-17 & 12-14 -> 11-12 & 17-14), delta=-4.152
pass 2: balik segmen posisi 12..14 (ganti sisi 6-8 & 4-9 -> 6-4 & 8-9), delta=-2.582
Biaya akhir: 155.742 km   (3 pass, 3 pertukaran)
```

Total perbaikan 9,345 km (5,7%) = jumlah ketiga delta (2,611 + 4,152 + 2,582 = 9,345 ✓). Pass terakhir tidak menemukan perbaikan, sehingga 2-opt berhenti di optimum lokal.

## 4. Correctness

| Algoritma | Argumen kebenaran | Asumsi |
|---|---|---|
| Dijkstra | Invarian: saat simpul *u* diambil dari heap dengan jarak *d*ᵤ, *d*ᵤ sudah jarak terpendek sesungguhnya. Bukti induksi: setiap jalur alternatif harus keluar dari himpunan simpul terkunci lewat sisi menuju simpul yang jaraknya sementara ≥ *d*ᵤ, dan bobot non-negatif tidak bisa memperkecilnya. | Bobot ≥ 0 (dijaga `Graph.add_edge`, TC05) |
| Held-Karp | Sub-struktur optimal: `dp[S][j] = min_{i∈S\{j}} dp[S\{j}][i] + d[i][j]`. Induksi pada \|S\|: tur optimal yang berakhir di *j* setelah mengunjungi *S* harus memakai jalur optimal ke predecessor-nya. | Matriks jarak lengkap (dijamin validasi keterjangkauan) |
| NN + 2-opt | **Validitas** terjamin (permutasi, depo tetap di posisi 0, TC09). **Optimalitas tidak dijamin**: hanya optimum lokal terhadap pertukaran 2 sisi. Terminasi dijamin karena tiap pertukaran menurunkan biaya > ε dan jumlah tur berhingga. | Jarak simetris (rumus delta memakai itu) |

Bukti empiris: Dijkstra = Floyd-Warshall (TC02, 5 graf × semua pasangan), Held-Karp = brute force (TC08, 8 instans), 2-opt ≤ NN dan ≥ optimum (TC09).

## 5. Kompleksitas

Notasi: V simpul, E ruas, k titik antar.

| Algoritma | Waktu | Ruang | Catatan dan pengaruh ukuran input |
|---|---|---|---|
| Dijkstra (heap) | O((V+E) log V) per sumber | O(V+E) | Dipanggil k+1 kali → O((k+1)(V+E) log V). Terukur: V 200→51.200 (×256) waktu 0,18→249 ms (×1.380), mendekati V log V |
| Held-Karp | O(k² 2ᵏ) | O(k 2ᵏ) | Tiap tambah 1 titik, waktu ≈ ×2–2,4 (terukur 381→891 ms dari k=15 ke 16, ×2,34). Memori: tabel `dp` dan `par` masing-masing k·2ᵏ sel → k=20 ≈ 21 juta sel per tabel (perkiraan, belum diukur) sehingga tidak layak di Python murni |
| Nearest Neighbor | O(k²) | O(k) | Terukur n=100→400 (×4) waktu 0,57→10,1 ms (×18, lebih besar dari ×16 teoretis karena overhead konstan dan cache) |
| 2-opt | O(k²) per pass, jumlah pass tidak berbatas polinomial secara teori | O(k) | Praktis 3 pass pada S4. Terukur NN+2-opt n=100→400: 3,6→83,9 ms |

Asumsi pengukuran: Python 3.13, satu inti, `time.perf_counter`, mesin cloud (angka absolut akan berbeda di mesin lain, tren yang relevan).
