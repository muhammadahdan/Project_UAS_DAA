# D13 – Checklist Paket Akhir LMS

**Yang sudah ada di repo (dibuat dan diverifikasi dengan eksekusi nyata):**

| Kode | Item | Status |
|---|---|---|
| D01 | Analisis kasus | Siap (Kelompok 1) |
| D02 | Matriks masalah–algoritma | Siap |
| D03 | Desain solusi | Siap |
| D04 | Source code | Siap, 41 tes lulus |
| D05 | Dataset, input dan output | Siap |
| D06 | Trace dan kompleksitas | Siap |
| D07 | Analisis komparatif | Siap |
| D08 | Test plan dan evidence | Siap |
| D09 | Laporan teknis PDF + petunjuk reproduksi | Siap (Kelompok 1) |
| D10 | Slide, pembagian tugas, skenario demo | Siap (**sesuaikan pembagian tugas dengan kenyataan**) |
| D11 | Naskah ilmiah | Draf siap, **pindahkan ke template JITUS resmi dan tambah penelitian terkait 2020–2026** |

**Yang harus Anda lakukan sendiri sebelum mengumpulkan:**

- [ ] Ganti semua placeholder `[NAMA ...]`, `[NIM]`, `[USERNAME]`, `[UNIVERSITAS]` (cari dengan `grep -rn "\[NAMA\|\[USERNAME\|\[ISI" .`)
- [ ] Isi nomor Week algoritma di D02 sesuai RPS
- [ ] Buat repo GitHub, push (lihat bawah), dan tempel URL repo di D09, D12, README
- [ ] Publikasikan artikel Medium (D12), isi URL dan tangkapan layar
- [ ] Setiap anggota unggah portofolio LinkedIn, isi URL dan tangkapan layar (D12)
- [ ] Pindahkan D11 ke template JITUS UPJ; tambahkan penelitian terkait yang benar-benar Anda baca
- [ ] **Setiap anggota membaca kode dan dokumen ini sampai paham**: viva individual akan meminta trace dan modifikasi sederhana
- [ ] Jalankan ulang `python -m pytest -q` dan `python scripts/run_experiments.py` di komputer Anda
- [ ] Susun paket LMS: D01–D12, source code, dataset, README, laporan, slide, bukti uji

## Push ke GitHub

```bash
cd rute-kurir-jakarta
git init -b main          # lewati bila sudah ada .git
git add .
git commit -m "UAS INF203: optimasi rute kurir Jakarta"
# buat repo kosong di github.com, lalu:
git remote add origin https://github.com/muhammadahdan/rute-kurir-jakarta.git
git push -u origin main
```

## Etika data (soal no. 5, butir 5)

Dataset sintetis: koordinat hanya pusat kawasan (informasi geografis publik). Tidak ada data pribadi, rahasia, atau kredensial di repo.
