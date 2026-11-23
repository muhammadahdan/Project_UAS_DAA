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
