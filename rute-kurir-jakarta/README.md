# Optimasi Rute Kurir Last-Mile Jakarta

Proyek UAS **INF203 – Desain dan Analisis Algoritma** (Gasal 2025/2026).
Menyusun urutan pengantaran kurir (satu depo, *k* titik antar, kembali ke depo) dengan jarak terpendek, memakai tiga algoritma yang **ditulis sendiri** (hanya pustaka standar Python):

| Algoritma | Peran | Kompleksitas |
|---|---|---|
| **Dijkstra** (binary heap) | Jarak terpendek antar titik pada graf jalan → matriks jarak | O((V+E) log V) per sumber |
| **Held-Karp** (DP bitmask) | Urutan kunjungan **optimal**, k ≤ 15 | O(k² 2ᵏ) waktu, O(k 2ᵏ) ruang |
| **Nearest Neighbor + 2-opt** | Urutan kunjungan cepat, k besar | O(k²) per pass |

> Data **sintetis** (42 lokasi Jakarta, ruas buatan). Hasil menggambarkan perilaku algoritma, bukan jarak jalan nyata.

## Hasil singkat (85 instans acak, k = 5…15)

| Metode | Selisih rata-rata dari optimum | Optimal ditemukan |
|---|---|---|
| Nearest Neighbor | 12,61% | – |
| NN + 2-opt | 1,03% | 63/85 |
| Held-Karp | 0% | 85/85 |

Rute Held-Karp rata-rata **37,1% lebih pendek** dari urutan masukan. Waktu: Held-Karp 381 ms (15 titik); NN+2-opt 1,5 ms (41 titik).

## Mulai cepat

```bash
git clone https://github.com/muhammadahdan/rute-kurir-jakarta.git
cd rute-kurir-jakarta
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt                       # matplotlib, pytest (Python 3.10+)

python -m pytest -q                                   # 41 tes
python -m rute.cli --scenario S2 --method auto        # Held-Karp: 122,613 km
python -m rute.cli --scenario S4 --method auto        # NN+2-opt: 155,742 km
python -m rute.cli --stops 3,8,15,22 --plot outputs/figures/rute_custom.png
```

Opsi `--method`: `auto` (k ≤ 15 → held_karp, selainnya nn2opt), `held_karp`, `nn`, `nn2opt`, `input` (baseline), `brute` (≤ 9 titik).
Skenario `S1…S5` (6, 10, 13, 25, 41 titik) ada di `data/scenarios.csv`.

## Mereproduksi semua hasil

```bash
python scripts/generate_data.py      # data/*.csv (deterministik, seed tetap)
python scripts/make_traces.py        # outputs/trace/*.txt
python scripts/run_experiments.py    # outputs/experiment_*.csv|md + gambar (~10 detik)
python scripts/make_flowchart.py     # outputs/figures/diagram_alur.png
```

## Struktur

```
rute/            kode sumber (D04): graph, dijkstra, tsp, cli, viz, data
tests/           pytest: 23 fungsi tes / 41 kasus (D08)
scripts/         pembangkit data, trace, eksperimen
data/            nodes.csv, edges.csv, scenarios.csv (D05)
outputs/         hasil eksperimen, trace, gambar, bukti tes & bug (D05, D06, D08)
docs/            D01–D13: analisis, desain, laporan PDF, slide, naskah JITUS, artikel
```

## Dokumen UAS

| Kode | Berkas |
|---|---|
| D01 | `docs/D01_analisis_kasus.md` |
| D02 | `docs/D02_matriks_masalah_algoritma.md` |
| D03 | `docs/D03_desain_solusi.md` |
| D04 | `rute/` (source code) |
| D05 | `data/`, `outputs/experiment_*.csv` |
| D06 | `docs/D06_trace_dan_kompleksitas.md`, `outputs/trace/` |
| D07 | `docs/D07_analisis_komparatif.md` |
| D08 | `docs/D08_test_plan_dan_evidence.md`, `outputs/test_evidence.txt`, `outputs/bug_evidence/` |
| D09 | `docs/D09_laporan_teknis.pdf` (+ sumber `.md`) |
| D10 | `docs/D10_slide_presentasi.pptx`, `docs/D10_pembagian_tugas_dan_demo.md` |
| D11 | `docs/D11_naskah_jitus.docx` (+ `.md`) |
| D12 | `docs/D12_artikel_medium.md`, `docs/D12_linkedin_dan_bukti_publikasi.md` |
| D13 | `docs/D13_checklist_pengumpulan.md` |

## Keterbatasan

Satu kendaraan tanpa kapasitas/jendela waktu/lalu lintas; Held-Karp tidak layak di atas ±20 titik; 2-opt hanya optimum lokal. Selengkapnya di D09 §7.

## Lisensi

MIT (lihat `LICENSE`).
