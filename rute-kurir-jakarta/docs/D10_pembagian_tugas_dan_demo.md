# D10 – Pembagian Tugas dan Skenario Live Demo

Slide: `D10_slide_presentasi.pptx` (14 slide, catatan pembicara di tiap slide).

## 1. Pembagian tugas

Dosen akan meminta **setiap anggota** menjelaskan kontribusi dan keputusan algoritmiknya secara individual, jadi bagian ini harus sesuai kenyataan. Usulan awal untuk 3 anggota:

| Anggota | Tanggung jawab utama | Berkas | Harus siap menjelaskan |
|---|---|---|---|
| [Muhammad Ahdanierrofie Ikhsan – 2025071008] | Graf, Dijkstra, dataset, matriks jarak | `rute/graph.py`, `rute/dijkstra.py`, `rute/data.py`, D01, D02 | Mengapa heap, mengapa bobot ≥ 0, trace Dijkstra, kompleksitas | NN, 2-opt, eksperimen, visualisasi | `rute/tsp.py` (NN, 2-opt), `scripts/`, D06, D07 | Rumus delta 2-opt, optimum lokal, hasil eksperimen |
| Bersama | Laporan D09, slide D10, artikel D11–D12, README | `docs/` | Seluruh alur solusi |
| [Muhammad Lutfi Hidayat – 2025071009] | Held-Karp, brute force pembanding, validasi, bug | `rute/tsp.py` (Held-Karp, validasi), `tests/`, D08 | Rumus DP, tabel `dp`/`par`, mengapa O(k² 2ᵏ), 4 bug dan perbaikannya | 

## 2. Skenario live demo (±8 menit)

Persiapan: `pip install -r requirements.txt`, lalu `python scripts/generate_data.py`.

| Langkah | Perintah | Hasil yang diharapkan (dari eksekusi nyata) |
|---|---|---|
| 1. Tes | `python -m pytest -q` | 41 passed |
| 2. Rute optimal | `python -m rute.cli --scenario S2 --method auto --plot outputs/figures/rute_S2.png` | held_karp, **122,613 km**, peta tersimpan |
| 3. Bandingkan heuristik | `python -m rute.cli --scenario S2 --method nn2opt` | **127,254 km** (selisih 3,8%), 2 pass, 4 pertukaran |
| 4. Titik besar | `python -m rute.cli --scenario S4 --method auto` | nn2opt, **155,742 km**, ±1 ms |
| 5. Masukan tidak valid | `python -m rute.cli --stops 3,999` | `Input tidak valid: titik 999 tidak dikenal di graf`, kode keluar 2 |
| 6. Trace | `python scripts/make_traces.py`, buka `outputs/trace/held_karp_4_titik.txt` | Tur 0→3→4→2→1→0 = 60,293 km |

## 3. Persiapan untuk permintaan dosen (perubahan input / modifikasi sederhana)

| Permintaan yang mungkin | Cara menanganinya |
|---|---|
| "Ganti titik antar" | `--stops 3,8,15,22` atau ubah baris di `data/scenarios.csv` |
| "Ganti depo" | `--depot 12 --stops ...` |
| "Tambah titik" | Tambahkan id; auto-switch Held-Karp ke heuristik di atas 15 titik (`hk_limit` di `rute/tsp.py`) |
| "Bagaimana kalau ruas diperpanjang?" | Ubah nilai `km` di `data/edges.csv`; jalankan ulang |
| "Tunjukkan trace manual" | Jelaskan tabel di D06 (graf 4 simpul untuk Dijkstra) |
| "Ubah 2-opt jadi best-improvement" | Di `two_opt()`, cari delta terkecil dulu di seluruh (i, j), baru balik |

**Cadangan bila demo gagal:** keluaran referensi sudah tersimpan di `outputs/` (CSV, trace, gambar).
