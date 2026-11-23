---
title: "Optimasi Rute Kurir Last-Mile di Jakarta Menggunakan Kombinasi Algoritma Dijkstra, Held-Karp, dan Nearest Neighbor dengan Perbaikan 2-opt"
author: "[Nama Penulis 1], [Nama Penulis 2], [Nama Penulis 3]"
date: "[Afiliasi: Program Studi Informatika, Universitas Pembangunan Jaya] · [email penulis korespondensi]"
---

**CATATAN PENYERAHAN (hapus sebelum dikumpulkan):** naskah ini mengikuti struktur yang diminta soal (pendahuluan, penelitian terkait, metode, hasil dan pembahasan, kesimpulan, referensi). **Template resmi JITUS UPJ tidak tersedia bagi saya**, jadi salin isi ke berkas template resmi dan sesuaikan gaya sitasi, margin, dan jumlah halaman. Bagian *Penelitian Terkait* menandai tempat Anda menambah artikel jurnal terbaru yang benar-benar Anda baca.

# Abstrak

Penyusunan urutan pengantaran yang tidak optimal meningkatkan jarak tempuh kurir dan biaya operasional. Penelitian ini membangun solusi optimasi rute satu kendaraan yang menggabungkan tiga algoritma: Dijkstra untuk jarak terpendek pada graf jalan, Held-Karp (pemrograman dinamis) untuk urutan kunjungan optimal pada hingga 15 titik, dan Nearest Neighbor dengan perbaikan 2-opt untuk jumlah titik yang lebih besar. Pengujian memakai dataset sintetis 42 lokasi di Jakarta dan 85 instans acak. Hasilnya, rute optimal rata-rata 37,1% lebih pendek daripada urutan masukan; Nearest Neighbor rata-rata 12,61% di atas optimum, sedangkan penambahan 2-opt menurunkannya menjadi 1,03% dan menemukan solusi optimal pada 63 dari 85 instans. Held-Karp tumbuh eksponensial (381 ms pada 15 titik; 891 ms pada 16 titik), sedangkan NN+2-opt memerlukan 84 ms pada 400 titik. Keterbatasan utama adalah data sintetis dan model tanpa kapasitas atau jendela waktu.

**Kata kunci:** optimasi rute, Dijkstra, Held-Karp, 2-opt, travelling salesman problem, last-mile delivery

# Abstract

Suboptimal delivery sequencing increases courier distance and operating cost. This study builds a single-vehicle route optimizer combining Dijkstra's algorithm for shortest paths on a road graph, the Held-Karp dynamic program for optimal tours of up to 15 stops, and Nearest Neighbor with 2-opt refinement for larger instances. Experiments use a synthetic 42-location Jakarta dataset and 85 random instances. Optimal routes are on average 37.1% shorter than the input order; Nearest Neighbor averages 12.61% above the optimum, while adding 2-opt reduces this to 1.03% and finds the optimum in 63 of 85 instances. Held-Karp grows exponentially (381 ms at 15 stops; 891 ms at 16), whereas NN+2-opt needs 84 ms for 400 stops. The main limitations are the synthetic data and the absence of capacity and time-window constraints.

**Keywords:** route optimization, Dijkstra, Held-Karp, 2-opt, travelling salesman problem, last-mile delivery

# 1. Pendahuluan

Pengiriman jarak terakhir (*last-mile*) merupakan komponen biaya besar dalam logistik, dan di kota padat seperti Jakarta urutan kunjungan yang buruk langsung menambah jarak tempuh. Banyak usaha kecil masih menyusun urutan secara manual atau mengikuti urutan pesanan. Masalah ini memiliki dua submasalah komputasi: (i) jarak terpendek antar-titik pada graf jalan, dan (ii) urutan kunjungan yang meminimalkan total jarak, yaitu *Travelling Salesman Problem* (TSP) yang bersifat NP-hard [1].

Tujuan penelitian ini adalah merancang, mengimplementasikan, dan mengevaluasi solusi yang (a) selalu menghasilkan rute valid, (b) menjamin optimum untuk instans kecil, (c) tetap cepat untuk instans besar, dan (d) menolak masukan tidak valid secara eksplisit. Kontribusinya adalah perbandingan terukur antara algoritma eksak dan heuristik pada submasalah TSP yang sama, serta analisis kontribusi Dijkstra sebagai penyedia matriks jarak.

# 2. Penelitian Terkait

Dijkstra [2] menyelesaikan jarak terpendek dari satu sumber pada graf berbobot non-negatif dan menjadi dasar banyak sistem navigasi. Untuk TSP, Held dan Karp [3] serta Bellman [4] mengajukan program dinamis dengan waktu O(n² 2ⁿ), jauh lebih baik daripada enumerasi O(n!) namun tetap eksponensial. Heuristik konstruktif seperti Nearest Neighbor dianalisis oleh Rosenkrantz dkk. [5], sedangkan perbaikan lokal 2-opt berasal dari Croes [6] dan dikembangkan lebih jauh oleh Lin dan Kernighan [7]. Pembahasan komprehensif tentang pemodelan dan metode penyelesaian rute kendaraan tersedia di Toth dan Vigo [8].

**[TAMBAHKAN 3–5 artikel jurnal/prosiding 2020–2026 tentang optimasi rute last-mile atau perbandingan solver TSP yang Anda baca langsung, lalu jelaskan perbedaannya dengan penelitian ini. Jangan mencantumkan referensi yang belum Anda baca.]**

# 3. Metode

**3.1 Data.** Dataset sintetis: 42 lokasi di Jakarta (koordinat perkiraan pusat kawasan), 79 ruas jalan dibangkitkan dari tiga tetangga terdekat dengan jarak garis lurus (haversine) dikalikan faktor kelokan acak 1,2–1,6 (seed 42), graf dijamin terhubung. Terdapat lima skenario pengantaran (6, 10, 13, 25, dan 41 titik). Tidak ada data pribadi.

**3.2 Alur solusi.** (1) validasi masukan: duplikat dan depo dibuang, id tidak dikenal ditolak; (2) Dijkstra dari tiap titik membangun matriks jarak terpendek; (3) titik tak terjangkau ditolak; (4) bila jumlah titik *k* ≤ 15 dipakai Held-Karp, selain itu Nearest Neighbor + 2-opt; (5) rekonstruksi jalur jalan dan total jarak.

**3.3 Algoritma.** *Dijkstra* dengan antrean prioritas biner, O((V+E) log V). *Held-Karp* dengan DP bitmask `dp[S][j] = min_i dp[S∖{j}][i] + d[i][j]`, O(k² 2ᵏ) waktu dan O(k 2ᵏ) ruang. *Nearest Neighbor* O(k²), diikuti *2-opt* yang membalik segmen tur bila selisih biaya `d[a][c] + d[b][e] − d[a][b] − d[c][e] < −ε`, O(k²) per pass. Seluruh algoritma diimplementasikan sendiri dalam Python 3.13 hanya dengan pustaka standar.

**3.4 Pengujian.** Kebenaran Dijkstra diverifikasi terhadap Floyd-Warshall, Held-Karp terhadap *brute force* (8 instans), serta 41 kasus uji normal, batas, dan tidak valid. Kualitas heuristik diukur sebagai selisih persentase terhadap biaya Held-Karp pada 85 instans acak (*k* = 5…15). Skalabilitas diukur dengan waktu eksekusi terhadap ukuran masukan.

# 4. Hasil dan Pembahasan

**4.1 Kualitas rute.** Tabel 1 merangkum perbandingan pada 85 instans.

*Tabel 1. Selisih terhadap optimum Held-Karp (85 instans)*

| Metode | Selisih rata-rata | Maksimum | Optimal ditemukan |
|---|---|---|---|
| Nearest Neighbor | 12,61% | 35,18% | – |
| NN + 2-opt | 1,03% | 13,47% | 63/85 (74%) |
| Held-Karp | 0% | 0% | 85/85 |

Rute optimal rata-rata 37,1% lebih pendek dari urutan masukan. Pada skenario S2 (10 titik), urutan masukan 159,61 km, NN+2-opt 127,25 km, dan optimum 122,61 km (selisih 3,8%). 2-opt tidak pernah menghasilkan rute lebih buruk dari Nearest Neighbor.

**4.2 Waktu dan ukuran masukan.** Waktu Held-Karp naik sekitar 2,3 kali setiap penambahan satu titik (381 ms pada 15 titik; 891 ms pada 16 titik), konsisten dengan O(k² 2ᵏ). NN+2-opt memerlukan kurang dari 0,1 ms pada *k* ≤ 15 dan 84 ms pada 400 titik. Dijkstra tumbuh mendekati O(V log V): waktu naik sekitar 1.380 kali ketika V naik 256 kali.

**4.3 Kontribusi algoritma.** Hanya 7–19% pasangan lokasi pada skenario uji yang memiliki ruas langsung, sehingga matriks jarak lengkap hanya dapat diperoleh melalui Dijkstra. Solver TSP tanpa langkah ini tidak dapat bekerja pada graf jarang.

**4.4 Pengujian dan *debugging*.** Draft awal gagal pada enam tes dari empat akar masalah: daftar titik kosong, duplikat/depo dalam daftar, id tidak dikenal, dan titik tak terjangkau. Yang terakhir paling berbahaya karena menghasilkan rute salah dengan biaya tak terhingga tanpa pesan galat. Seluruh bug diperbaiki dan 41 tes lulus.

**4.5 Keterbatasan.** Data sintetis; satu kendaraan tanpa kapasitas, jendela waktu, maupun lalu lintas; Held-Karp tidak layak untuk *k* di atas sekitar 20; 2-opt hanya optimum lokal (22 dari 85 instans tidak optimal); instans *k* = 14 dan 15 hanya 3 dan 2 sehingga hanya bersifat indikatif.

# 5. Kesimpulan

Kombinasi Dijkstra, Held-Karp, dan Nearest Neighbor + 2-opt menghasilkan rute valid yang rata-rata 37,1% lebih pendek daripada urutan masukan, dengan heuristik hanya 1,03% di atas optimum dan waktu di bawah satu detik pada seluruh skenario. Pekerjaan lanjutan meliputi data jalan nyata (OpenStreetMap), kapasitas dan jendela waktu (VRP), serta heuristik Or-opt atau Lin-Kernighan.

# Referensi

[1] G. Dantzig, R. Fulkerson, and S. Johnson, "Solution of a large-scale traveling-salesman problem," *Journal of the Operations Research Society of America*, vol. 2, no. 4, pp. 393–410, 1954.

[2] E. W. Dijkstra, "A note on two problems in connexion with graphs," *Numerische Mathematik*, vol. 1, pp. 269–271, 1959.

[3] M. Held and R. M. Karp, "A dynamic programming approach to sequencing problems," *Journal of the SIAM*, vol. 10, no. 1, pp. 196–210, 1962.

[4] R. Bellman, "Dynamic programming treatment of the travelling salesman problem," *Journal of the ACM*, vol. 9, no. 1, pp. 61–63, 1962.

[5] D. J. Rosenkrantz, R. E. Stearns, and P. M. Lewis, "An analysis of several heuristics for the traveling salesman problem," *SIAM Journal on Computing*, vol. 6, no. 3, pp. 563–581, 1977.

[6] G. A. Croes, "A method for solving traveling-salesman problems," *Operations Research*, vol. 6, no. 6, pp. 791–812, 1958.

[7] S. Lin and B. W. Kernighan, "An effective heuristic algorithm for the traveling-salesman problem," *Operations Research*, vol. 21, no. 2, pp. 498–516, 1973.

[8] P. Toth and D. Vigo, Eds., *Vehicle Routing: Problems, Methods, and Applications*, 2nd ed. Philadelphia, PA, USA: SIAM, 2014.
