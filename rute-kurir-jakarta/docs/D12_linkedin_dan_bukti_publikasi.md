# D12 – Bukti Publikasi Medium dan Portofolio LinkedIn

Saya (Claude) tidak bisa mempublikasikan ke Medium atau LinkedIn atas nama Anda. Naskah siap pakai ada di sini; **setelah Anda mempublikasikan, isi tabel bukti di bawah.**

## 1. Bukti publikasi (ISI SETELAH PUBLIKASI)

| Item | URL | Tanggal | Screenshot |
|---|---|---|---|
| Artikel Medium (naskah: `D12_artikel_medium.md`) | [ISI URL] | [ISI] | `docs/bukti/medium.png` |
| LinkedIn [Anggota 1] | [ISI URL] | [ISI] | `docs/bukti/linkedin_1.png` |
| LinkedIn [Anggota 2] | [ISI URL] | [ISI] | `docs/bukti/linkedin_2.png` |
| LinkedIn [Anggota 3] | [ISI URL] | [ISI] | `docs/bukti/linkedin_3.png` |
| Repository GitHub | [ISI URL] | [ISI] | – |

## 2. Template portofolio LinkedIn (satu per anggota, ubah sesuai peran pribadi)

Setiap anggota perlu menjelaskan **peran pribadi**, solusi, algoritma, temuan, dan tautan. Tulis dengan kata Anda sendiri dan hanya klaim yang benar-benar Anda kerjakan.

### Bagian "Projects" / "Featured"

**Judul:** Optimasi Rute Kurir Last-Mile Jakarta: Dijkstra, Held-Karp, dan 2-opt

**Deskripsi (contoh untuk Anggota 1, Dijkstra/data):**

> Proyek UAS Desain dan Analisis Algoritma (kelompok 3 orang). Kami merancang pencari rute kurir untuk 42 lokasi di Jakarta (data sintetis). Peran saya: mengimplementasikan Dijkstra dengan heap dari nol, membangun graf dan dataset, serta menurunkan matriks jarak yang menjadi masukan solver TSP. Gabungan Dijkstra, Held-Karp (optimal sampai 15 titik) dan Nearest Neighbor + 2-opt menghasilkan rute rata-rata 37% lebih pendek dari urutan masukan; heuristik hanya 1,0% di atas optimum pada 85 instans uji. Saya juga belajar bahwa kasus tepi (titik tak terjangkau) bisa menghasilkan jawaban salah tanpa galat. Kode dan artikel: [URL GitHub] · [URL Medium]

**Skills:** Algorithm Design, Dynamic Programming, Graph Algorithms, Python, Testing (pytest)

### Variasi peran

| Anggota | Kalimat peran (sesuaikan) |
|---|---|
| Anggota 2 (Held-Karp, tes) | "Saya mengimplementasikan Held-Karp (DP bitmask), memverifikasinya terhadap brute force, dan menemukan serta memperbaiki empat bug dari edge-case test." |
| Anggota 3 (NN, 2-opt, eksperimen) | "Saya mengimplementasikan Nearest Neighbor dan 2-opt, merancang eksperimen 85 instans, dan menganalisis trade-off kualitas vs waktu (selisih 12,6% → 1,0%)." |

### Posting singkat (opsional)

> Baru selesai proyek UAS Desain dan Analisis Algoritma: optimasi rute kurir Jakarta dengan Dijkstra, Held-Karp, dan 2-opt. Temuan favorit saya: heuristik 2-opt rata-rata hanya 1% dari optimum, tapi bug yang paling berbahaya justru yang tidak menimbulkan error. Artikel: [URL] · Kode: [URL] #algoritma #python #optimasi
