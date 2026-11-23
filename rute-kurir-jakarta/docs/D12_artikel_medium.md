# Cara Kami Memangkas Jarak Kurir 37%: Dijkstra, Held-Karp, dan 2-opt di Jakarta

*Oleh [Kelompok 1]: [Muhammad Ahdanierrofie Ikhsan] (Dijkstra dan data, Nearest Neighbor, 2-opt, dan eksperimen), [Muhammad Lutfi Hidayat] (Held-Karp dan pengujian). Proyek UAS Desain dan Analisis Algoritma, [UNIVERSITAS].*

---

Bayangkan seorang kurir UMKM di Jakarta yang harus mengantar 10 paket. Ia berangkat dari Kemayoran dan mengikuti urutan pesanan masuk. Hasilnya: 159,6 km. Dengan urutan yang dioptimalkan, rute yang sama hanya 122,6 km, 23% lebih pendek. Selisih 37 km itu adalah bensin dan waktu yang terbuang setiap hari.

Kami membangun alat kecil untuk menyusun urutan itu, dan di sepanjang jalan belajar bahwa tiga algoritma klasik ternyata bisa saling melengkapi.

## Kasusnya

Satu kurir, satu depo, *k* titik antar, pulang ke depo, total jarak sependek mungkin. Ada dua submasalah:

1. **Berapa jarak terpendek antar dua titik?** Antar titik jarang punya ruas langsung. Di dataset kami hanya 7–19% pasangan lokasi yang terhubung langsung.
2. **Urutan mana yang terbaik?** Ini *Travelling Salesman Problem* (TSP), NP-hard.

> Catatan jujur: data kami **sintetis** (42 lokasi di Jakarta dengan ruas buatan, bukan peta jalan asli). Angka di sini menggambarkan perilaku algoritma, bukan jarak jalan sebenarnya.

## Tiga algoritma, tiga peran

**1. Dijkstra, menyediakan jarak.** Dijalankan dari tiap titik antar untuk membangun matriks jarak terpendek. Kami memilihnya daripada Floyd-Warshall karena hanya butuh *k*+1 sumber dari 42 simpul dan grafnya jarang.

**2. Held-Karp, jawaban pasti.** Program dinamis dengan bitmask: `dp[S][j]` = biaya terkecil dari depo, mengunjungi himpunan S, berakhir di j. Waktunya O(k² 2ᵏ). Kami mengukur 381 ms untuk 15 titik dan 891 ms untuk 16. Waktu naik sekitar 2,3 kali setiap tambah satu titik.

**3. Nearest Neighbor + 2-opt, jawaban cepat.** Nearest Neighbor membangun rute awal dengan selalu ke titik terdekat. 2-opt lalu membalik potongan rute selama itu memperpendek total jarak, dan menghilangkan rute yang saling bersilang.

## Cara kerjanya (contoh yang bisa dicek dengan tangan)

Pada graf kecil A–B=4, A–C=1, C–B=2, B–D=1, Dijkstra pertama menemukan B berjarak 4, lalu memperbaikinya jadi 3 setelah C dikunci (jalur A-C-B). Jarak ke D akhirnya 4, bukan 6.

Untuk Held-Karp dengan 4 titik, tur optimum Kemayoran → Kebon Jeruk → Cawang → Cempaka Putih → Sunter → Kemayoran bernilai 14,41 + 19,42 + 14,48 + 7,65 + 4,34 = 60,30 km. Program menghasilkan 60,293 km.

## Hasil uji

Kami menguji 85 instans acak (5–15 titik antar) dan membandingkan dengan Held-Karp sebagai jawaban optimum:

| Metode | Selisih rata-rata dari optimum | Terburuk | Optimal ditemukan |
|---|---|---|---|
| Nearest Neighbor | 12,6% | 35,2% | – |
| NN + 2-opt | **1,0%** | 13,5% | 74% |

Rata-rata, rute optimal 37% lebih pendek dari urutan masukan. Untuk 41 titik, NN+2-opt selesai dalam sekitar 1,5 ms, sementara Held-Karp tidak mungkin dipakai di skala itu.

Catatan: pada 14 dan 15 titik, instans yang kami uji hanya 3 dan 2 (Held-Karp mahal), jadi angka di sana hanya indikasi.

## Yang kami pelajari

- **Heuristik sederhana bisa sangat baik, tetapi tanpa jaminan.** 2-opt menemukan solusi optimal di 74% instans, tapi pernah 13,5% lebih buruk.
- **Algoritma eksak tetap berguna** sebagai tolok ukur kebenaran. Kami memakainya untuk memverifikasi heuristik.
- **Bug paling berbahaya adalah yang diam.** Pada draft awal, titik yang tidak terjangkau menghasilkan biaya tak terhingga dan rute yang memangkas titik, tanpa pesan galat. Uji edge case menemukannya, bersama tiga bug lain: daftar kosong, titik duplikat, dan id tidak dikenal.
- **Jangan paksakan algoritma.** Held-Karp kami batasi sampai 15 titik; sisanya heuristik.

## Coba sendiri

Kode, data, tes, dan laporan lengkap: **https://github.com/[USERNAME]/rute-kurir-jakarta**

```bash
pip install -r requirements.txt
python -m rute.cli --scenario S2 --method auto
```

## Kontribusi anggota

- **[Anggota 1]:** graf, Dijkstra, dataset sintetis.
- **[Anggota 2]:** Held-Karp, validasi masukan, pengujian dan debugging.
- **[Anggota 3]:** Nearest Neighbor, 2-opt, eksperimen, visualisasi.

*Referensi: Dijkstra (1959); Held & Karp (1962); Croes (1958); Rosenkrantz, Stearns & Lewis (1977).*
