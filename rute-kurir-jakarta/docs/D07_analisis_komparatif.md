# D07 – Analisis Komparatif dan Kontribusi Algoritma

Semua angka berasal dari `scripts/run_experiments.py` (seed tetap). Tabel lengkap: `outputs/experiment_report.md`.

## 1. Algoritma saling melengkapi: kontribusi Dijkstra

Dijkstra tidak bersaing dengan TSP solver; ia menyediakan masukannya. Ilustrasi kontribusinya: pada skenario S1 hanya 4 dari 21 pasangan lokasi (19%) yang punya ruas langsung, dan pada S2–S5 hanya 7–12%. Sisanya hanya bisa dihitung lewat jalur terpendek (mis. Sunter→Cempaka Putih = 7,65 km lewat simpul perantara, karena tidak ada ruas langsung). Tanpa langkah ini, Held-Karp/NN tidak punya matriks jarak yang lengkap.

Waktu Dijkstra untuk membangun matriks sangat kecil dibanding fase TSP pada *k* besar: S5 (41 titik) total 1,5 ms termasuk Dijkstra + NN + 2-opt.

## 2. Algoritma menyelesaikan submasalah sama (TSP): Held-Karp vs NN vs NN+2-opt

Eksperimen A: 85 instans acak (k = 5…15; 10 instans untuk k ≤ 11, 5 untuk k = 12–13, 3 untuk k = 14, 2 untuk k = 15), acuan = biaya Held-Karp (optimal).

| k | n | Hemat Held-Karp vs urutan input | Selisih NN rata-rata | Selisih NN+2-opt rata-rata | NN+2-opt maks | Optimal ditemukan 2-opt | Waktu heuristik | Waktu Held-Karp |
|---|---|---|---|---|---|---|---|---|
| 5 | 10 | 18,0% | 8,97% | 0,00% | 0,00% | 10/10 | 0,014 ms | 0,06 ms |
| 8 | 10 | 31,7% | 13,57% | 1,40% | 13,47% | 6/10 | 0,023 ms | 0,86 ms |
| 10 | 10 | 40,0% | 12,96% | 0,87% | 5,67% | 7/10 | 0,038 ms | 5,34 ms |
| 12 | 5 | 46,0% | 13,80% | 1,36% | 6,82% | 4/5 | 0,065 ms | 29,6 ms |
| 13 | 5 | 48,6% | 14,18% | 3,27% | 8,49% | 2/5 | 0,081 ms | 79,4 ms |
| 15 | 2 | 56,4% | 20,20% | 4,27% | 8,54% | 1/2 | 0,094 ms | 381,5 ms |
| **Seluruh 85 instans** | 85 | **37,1%** | **12,61%** | **1,03%** | **13,47%** | **63/85 (74%)** | | |

Gambar: `outputs/figures/gap_vs_k.png` dan `outputs/figures/waktu_vs_ukuran.png`.

**Trade-off yang teramati**

- **Kualitas:** NN murni rata-rata 12,6% lebih panjang dari optimum (maks 35,2%). Menambah 2-opt menurunkannya ke 1,0% rata-rata dan menemukan solusi optimal pada 74% instans. 2-opt tidak pernah lebih buruk dari NN.
- **Waktu:** Held-Karp tumbuh eksponensial (k = 10: 5 ms → k = 15: 381 ms → k = 16: 891 ms), sementara NN+2-opt tetap di bawah 0,1 ms pada k ≤ 15 dan 84 ms pada 400 titik.
- **Kapan Held-Karp tetap unggul:** bila jaminan optimal diperlukan dan k ≤ 15, biayanya masih di bawah satu detik. Untuk S2, 2-opt menghasilkan 127,25 km sementara optimum 122,61 km (selisih 3,8%, setara 4,6 km per hari per kurir).
- **Kapan heuristik dipilih:** k > 15, atau bila dibutuhkan jawaban cepat berulang (mis. simulasi banyak skenario).

## 3. Hasil per skenario (dataset `data/scenarios.csv`)

| Skenario | k | Urutan input (km) | NN (km) | NN+2-opt (km) | Held-Karp (km) | Hemat NN+2-opt vs input |
|---|---|---|---|---|---|---|
| S1 | 6 | 87,29 | 77,14 | 72,82 | 72,82 | 16,6% |
| S2 | 10 | 159,61 | 147,00 | 127,25 | 122,61 | 20,3% |
| S3 | 13 | 160,32 | 130,09 | 123,23 | 118,90 | 23,1% |
| S4 | 25 | 276,74 | 165,09 | 155,74 | – (di luar batas) | 43,7% |
| S5 | 41 | 369,64 | 242,81 | 193,18 | – (di luar batas) | 47,7% |

## 4. Kondisi ketika pendekatan kurang tepat (jangan dipaksakan)

- **Held-Karp untuk k > 15:** waktu dan memori eksponensial. Dihindari oleh pemilih otomatis (`auto`).
- **NN+2-opt bila optimum wajib:** tidak ada jaminan. Pada 22 dari 85 instans hasilnya tidak optimal; maksimum selisih 13,47%.
- **Heuristik pada k sangat kecil (≤ 5):** tidak perlu, Held-Karp hanya 0,06 ms.
- **Dijkstra:** tidak cocok bila ada bobot negatif; tidak relevan untuk jarak jalan nyata.
- Algoritma lain dari Week 01–15 (mis. MST, backtracking murni) tidak dimasukkan karena tidak memberi kontribusi pada kasus ini.

## 5. Catatan validitas data eksperimen

- Instans k = 14 dan 15 hanya 3 dan 2 buah (Held-Karp mahal). Selisih rata-rata pada k tersebut adalah indikasi, bukan estimasi statistik yang kuat.
- Dataset sintetis; hasil dengan jarak jalan nyata (OpenStreetMap, lalu lintas) bisa berbeda.
