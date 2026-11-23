# D01 – Analisis Kasus

**MK INF203 – Desain dan Analisis Algoritma · UAS Gasal 2025/2026**
**Kelompok:** [Kelompok 1] · **Anggota:** [Muhammad Ahdanierrofie Ikhsan – 2025071008] · [Muhammad Lutfi Hidayat – 2025071009]

## 1. Studi kasus

**Optimasi rute kurir last-mile di Jakarta.** Satu kurir berangkat dari depo (Kemayoran), harus mengantar paket ke sejumlah titik tersebar di Jakarta, lalu kembali ke depo. Urutan kunjungan yang buruk membuat kurir menempuh jarak jauh lebih panjang, sehingga biaya bahan bakar dan waktu kerja membengkak. Ini masalah nyata yang dihadapi hampir semua jasa pengiriman dan UMKM yang mengantar sendiri.

## 2. Konteks dan pengguna

| Aspek | Uraian |
|---|---|
| Konteks | Pengiriman paket harian dalam kota, satu kendaraan, satu depo |
| Pengguna | Koordinator pengiriman di UMKM/gudang kecil yang menyusun rute harian kurir |
| Kebutuhan pengguna | Urutan kunjungan dengan total jarak sependek mungkin, dihitung dalam hitungan detik, dan dapat dipercaya (rute valid, tidak ada titik terlewat) |
| Kondisi saat ini | Urutan ditentukan manual / sesuai urutan pesanan masuk |

## 3. Problem statement

Diberikan graf jalan tidak berarah berbobot jarak (km), satu depo, dan sekumpulan *k* titik antar, tentukan urutan kunjungan yang mengunjungi setiap titik tepat satu kali dan kembali ke depo dengan **total jarak lintasan jalan minimum**.

Masalah ini punya dua submasalah komputasi:

1. **Jarak terpendek antar-titik** pada graf jalan (shortest path). Antar titik antar belum tentu ada ruas langsung, sehingga jarak harus dihitung lewat jalur terpendek.
2. **Urutan kunjungan** (Travelling Salesman Problem, TSP) di atas matriks jarak tersebut. Ini NP-hard.

## 4. Input, output, batasan

| | |
|---|---|
| **Input** | Graf jalan: `data/nodes.csv` (42 lokasi, id, nama, lat, lon) dan `data/edges.csv` (79 ruas, km). Depo (id 0). Daftar *k* id titik antar (`data/scenarios.csv` atau `--stops`). |
| **Output** | Urutan kunjungan, jalur jalan lengkap (simpul demi simpul), total jarak (km), waktu hitung (ms) |
| **Batasan model** | Satu kendaraan; jarak simetris (ruas dua arah); bobot non-negatif; tanpa kapasitas muatan, jendela waktu, kemacetan, atau jalan satu arah; graf harus terhubung untuk titik yang diminta |
| **Batasan data** | Dataset **sintetis**: koordinat = perkiraan pusat kawasan (informasi geografis publik), ruas = 3 tetangga terdekat dengan faktor kelokan acak 1,2–1,6 (seed 42). Bukan jarak jalan asli. Tidak ada data pribadi. |
| **Batasan komputasi** | Hasil eksak hanya layak untuk *k* kecil (Held-Karp memakai memori O(k·2^k)) |

## 5. Kriteria keberhasilan (terukur)

| # | Kriteria | Cara ukur | Hasil (lihat D06/D07/D08) |
|---|---|---|---|
| K1 | Rute valid: setiap titik tepat satu kali, mulai dan akhir di depo | Tes otomatis TC08–TC15 | Terpenuhi |
| K2 | Solusi eksak (Held-Karp) cocok dengan brute force | TC08, 8 instans acak | Terpenuhi (8/8) |
| K3 | Rata-rata total jarak ≥ 15% lebih pendek dari urutan masukan | Eksperimen A, 85 instans | Rata-rata 37,1% lebih pendek (1 instans k=5 kebetulan sudah optimal, penghematan 0%) |
| K4 | Heuristik (NN+2-opt) selisih rata-rata ≤ 5% dari optimum untuk *k* ≤ 15 | Eksperimen A | Rata-rata 1,03% (maks 13,47%) |
| K5 | Waktu ≤ 1 detik untuk 41 titik (heuristik) dan ≤ 15 titik (eksak) | Eksperimen B/C | 1,5 ms (41 titik); 381 ms (15 titik) |
| K6 | Masukan tidak valid ditolak dengan pesan jelas, bukan hasil salah diam-diam | TC16–TC19, TC23 | Terpenuhi setelah perbaikan BUG-1…4 |

## 6. Ruang lingkup yang sengaja tidak dicakup

Kapasitas kendaraan dan multi-kurir (VRP), jendela waktu, lalu lintas dinamis, data jalan nyata (OpenStreetMap). Ini dibahas sebagai keterbatasan di D09.
