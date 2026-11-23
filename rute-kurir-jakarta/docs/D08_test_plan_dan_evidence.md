# D08 – Test Plan dan Evidence

Jalankan: `python -m pytest -v`. Bukti eksekusi: `outputs/test_evidence.txt` (final) dan `outputs/bug_evidence/` (sebelum dan sesudah perbaikan).
Hasil final: **23 fungsi tes (41 kasus uji termasuk parametrisasi), semuanya lulus.**

## 1. Daftar test case

Kolom *Actual* = hasil eksekusi **pertama** pada draft awal kode (`run1_draft_pertama.txt`); kolom *Status* = status setelah perbaikan (`run2_setelah_perbaikan.txt`).

| ID | Jenis | Input | Expected | Actual (draft awal) | Status final | Bukti |
|---|---|---|---|---|---|---|
| TC01 | Normal | Graf 5 simpul (4 terhubung), sumber A | A→B=3, A→D=4, jalur A-C-B-D (dihitung tangan) | Sesuai | LULUS | test_dijkstra.py |
| TC02 | Normal | 5 graf acak 25 simpul | Dijkstra = Floyd-Warshall semua pasangan | Sesuai | LULUS | test_dijkstra.py |
| TC03 | Batas | sumber = tujuan | jarak 0 | Sesuai | LULUS | |
| TC04 | Batas | simpul terisolasi | jarak inf | Sesuai | LULUS | |
| TC05 | Tidak valid | ruas bobot −1 | `ValueError` | Sesuai | LULUS | |
| TC06 | Data | Graf Jakarta, sumber depo | 42 simpul semua terjangkau | Sesuai | LULUS | |
| TC07 | Normal | 4 titik persegi 1×1 | biaya 4,0 | Sesuai | LULUS | test_tsp.py |
| TC08 | Normal | 8 instans acak, 7 titik antar | biaya Held-Karp = brute force | Sesuai | LULUS | |
| TC09 | Normal | 8 instans, 10 titik antar | 2-opt valid, ≤ NN, ≥ optimum | Sesuai | LULUS | |
| TC10 | Normal | 6 titik, Held-Karp | biaya = jumlah ruas `road_path`; mulai/akhir depo | Sesuai | LULUS | |
| TC11 | Normal | 6 titik urutan acak | optimum ≤ urutan input | Sesuai | LULUS | |
| TC12 | Batas | `stops=[]` | rute `[depo]`, biaya 0 | **`ValueError: min() iterable argument is empty`** | LULUS (BUG-1) | run1 → run2 |
| TC13 | Batas | 1 titik | pergi-pulang, HK = nn2opt | Sesuai | LULUS | |
| TC14 | Batas | 2 titik | HK = brute = nn2opt | Sesuai | LULUS | |
| TC15 | Batas | semua 41 lokasi, nn2opt | tiap lokasi tepat 1× | Sesuai | LULUS | |
| TC16 | Tidak valid | `[3, 8, 3, 15, 8]` | duplikat dibuang, = hasil `[3, 8, 15]` | **order `[0, 3, 3, 8, 8, 15]`** | LULUS (BUG-2) | |
| TC17 | Tidak valid | `[0, 3, 8]` (depo di daftar) | depo hanya sekali | **order `[0, 8, 3, 0]`** (depo 2×) | LULUS (BUG-2) | |
| TC18 | Tidak valid | `[3, 999]` | `ValueError` "tidak dikenal" | **`KeyError: 999`** (galat mentah) | LULUS (BUG-3) | |
| TC19 | Tidak valid | titik terisolasi | `ValueError` "tidak terjangkau" | **Tidak ada galat; biaya `inf`, order `[0, 1]`** | LULUS (BUG-4) | |
| TC20 | Tidak valid | metode "ajaib" | `ValueError` | Sesuai | LULUS | |
| TC21 | Normal | CLI `--scenario S1` | kode keluar 0, ada "Total jarak" | Sesuai | LULUS | test_cli.py |
| TC22 | Tidak valid | CLI skenario S99 | kode keluar 2 | Sesuai | LULUS | |
| TC23 | Tidak valid | CLI `--stops 3,999` | kode keluar 2 + pesan "Input tidak valid" | **`KeyError` tidak tertangani** | LULUS (BUG-3) | |

## 2. Verifikasi kebenaran terhadap rujukan independen

| Komponen | Rujukan | Hasil |
|---|---|---|
| Dijkstra | Floyd-Warshall (ditulis terpisah di `tests/conftest.py`), 5 graf × semua pasangan | Cocok (tol. 1e-9) |
| Held-Karp | Brute force semua permutasi, 8 instans | Cocok |
| Held-Karp | Contoh manual persegi 1×1 dan trace 4 titik (D06: 60,30 km dihitung tangan) | Cocok |
| Biaya rute | Penjumlahan ulang panjang ruas pada `road_path` | Cocok (TC10) |
| Heuristik | Held-Karp sebagai optimum, 85 instans | 2-opt tidak pernah di bawah optimum dan tidak pernah lebih buruk dari NN |
| Performa vs ukuran | `outputs/experiment_scaling.csv` | Lihat D06/D07 |

## 3. Bug yang ditemukan, penyebab, perbaikan, uji ulang

Draft pertama `solve()` sengaja ditulis ringkas (tanpa validasi), lalu diuji dengan test edge case. Enam tes gagal (`outputs/bug_evidence/run1_draft_pertama.txt`), berasal dari empat akar masalah:

| Bug | Gejala | Penyebab | Perbaikan | Uji ulang |
|---|---|---|---|---|
| **BUG-1** daftar titik kosong | `ValueError: min() iterable argument is empty` di `held_karp` (TC12) | Dengan `k=0`, `range(m)` kosong sehingga `min()` tidak punya elemen | Guard di awal `held_karp`: bila `m == 0` kembalikan `(0.0, [0])` | TC12 lulus |
| **BUG-2** duplikat / depo di daftar titik | Rute memuat titik ganda (`[0,3,3,8,8,15]`) dan depo dua kali (`[0,8,3,0]`) (TC16, TC17) | Daftar masukan dipakai apa adanya sebagai simpul TSP | `validate_stops()` membuang duplikat dan depo dengan menjaga urutan pertama | TC16, TC17 lulus |
| **BUG-3** id tidak dikenal | `KeyError: 999` mentah; CLI crash (TC18, TC23) | `dist[t]` diakses tanpa memeriksa id | `validate_stops()` melempar `ValueError("titik 999 tidak dikenal di graf")`; CLI menangkapnya (kode keluar 2) | TC18, TC23 lulus |
| **BUG-4** titik tak terjangkau | **Hasil salah diam-diam:** biaya `inf` dan rute `[0, 1]` tanpa galat (TC19) | Jarak `inf` ikut masuk DP; `min()` memilih elemen pertama; rekonstruksi berhenti di parent `-1` | Setelah matriks dibangun, `solve()` memeriksa `d[0][j] == inf` → `ValueError("tidak terjangkau")` | TC19 lulus |

BUG-4 paling berbahaya karena tidak menimbulkan galat: pengguna mendapat rute tanpa tahu titik terlewat.

Hasil uji ulang setelah semua perbaikan: **41 lulus, 0 gagal** (`run2_setelah_perbaikan.txt`).

## 4. Evaluasi performa pada variasi ukuran

Lihat `outputs/experiment_scaling.csv` dan `outputs/figures/waktu_vs_ukuran.png` (diringkas di D06 §5 dan D07 §2).
