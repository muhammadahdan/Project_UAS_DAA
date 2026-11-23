# D02 – Matriks Masalah–Algoritma–Alasan Pemilihan

Tiga algoritma dari materi Week 01–15 dipilih. **Dijkstra** dan **Held-Karp/NN+2-opt** menyelesaikan submasalah berbeda (saling melengkapi). **Held-Karp** dan **NN+2-opt** menyelesaikan submasalah yang sama (dibandingkan).

> Isi kolom "Week" sesuai RPS INF203 kelompok Anda.

| Submasalah | Algoritma terpilih | Paradigma (Week) | Fungsi dalam solusi | Alternatif yang dipertimbangkan | Alasan pemilihan (berdasarkan data & tujuan) |
|---|---|---|---|---|---|
| Jarak terpendek antar titik pada graf jalan | **Dijkstra** (binary heap) | Greedy / graf (Week [..]) | Menghasilkan matriks jarak *d* antara depo dan semua titik antar, plus jalur jalan untuk rekonstruksi rute | BFS (hanya untuk graf tak berbobot, salah di sini); Bellman-Ford O(VE) (perlu hanya bila ada bobot negatif, tidak ada di data jalan); Floyd-Warshall O(V³) (menghitung semua pasangan, padahal hanya k+1 simpul dari 42 yang dibutuhkan) | Bobot jarak non-negatif, graf jarang (E ≈ 1,9V), sumber hanya k+1 → k+1 kali Dijkstra O((k+1)(V+E) log V) lebih hemat dari Floyd-Warshall |
| Urutan kunjungan optimum, *k* kecil (≤ 15) | **Held-Karp** (DP bitmask) | Dynamic programming (Week [..]) | Menghasilkan tur **optimal** sebagai acuan kebenaran dan solusi utama untuk rute kecil | Brute force O(k!) (layak hanya k ≤ 9–10); branch & bound (lebih rumit, tidak ada jaminan lebih cepat di kasus terburuk) | Sub-struktur optimal jelas; k dari pengguna UMKM biasanya kecil; butuh jaminan optimal |
| Urutan kunjungan, *k* besar (> 15) | **Nearest Neighbor + 2-opt** | Greedy + perbaikan lokal (Week [..]) | NN membangun tur awal cepat; 2-opt menghilangkan persilangan rute | Held-Karp (memori/waktu eksponensial); algoritma aproksimasi Christofides (butuh MST+matching, implementasi lebih berat); NN saja (selisih rata-rata 12,6% dari optimum) | Waktu polinomial O(k²) per pass; kualitas jauh lebih baik dari NN murni; implementasi sederhana dan dapat dijelaskan secara individual |

## Bagaimana ketiganya bekerja sama

```
Dijkstra  ──(matriks d)──►  Held-Karp   (k ≤ 15, optimal)
                         └► NN + 2-opt  (k > 15, heuristik)
```

- **Saling melengkapi:** Dijkstra tidak bisa menentukan urutan kunjungan; TSP solver tidak bisa bekerja tanpa matriks jarak. Tanpa Dijkstra, solver TSP akan salah mengira antar-titik tanpa ruas langsung sebagai tak terhingga.
- **Dibandingkan:** Held-Karp vs NN+2-opt pada instans yang sama (D07).

## Algoritma yang sengaja TIDAK dipakai
Algoritma yang tidak relevan tidak dipaksakan: misalnya MST/Kruskal tidak menyelesaikan TSP secara langsung, dan hanya akan dipakai bila diperlukan untuk aproksimasi Christofides.
