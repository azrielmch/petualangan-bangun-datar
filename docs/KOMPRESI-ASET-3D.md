# Kompresi lossless aset 3D

Alat: `tools/compress_assets_lossless.py` (Python dan Pillow).

```sh
python3 tools/compress_assets_lossless.py
```

- Memproses PNG di `assets-3d/` dan PNG base64 yang ditanam di dalam SVG.
- Tidak mengubah dimensi, mode piksel, palet, transparansi, atau profil warna.
- Mempertahankan semua chunk metadata PNG di luar IDAT, serta markup SVG di luar payload gambar.
- Setiap PNG diverifikasi memiliki sampel piksel identik sebelum/sesudah. Hasil yang tidak lebih kecil tidak dipakai.
- Tidak mengubah nama atau jalur aset, konfigurasi game, maupun aturan permainan.
- Ringkasan ukuran dan daftar perubahan disimpan di `docs/ASSET-3D-COMPRESSION.json`.
- Metadata dipertahankan secara byte, tetapi validitas tanda tangan/provenance yang mengikat byte file tidak dijamin setelah pengodean ulang.

Jalankan ulang setelah pembangun aset membuat ulang PNG/SVG. Sumber di arsip tidak diubah. Publikasi ke GitHub/Vercel dilakukan terpisah saat diminta.
