# Pengelompokan file lokal

Folder `kelompok-lokal/` menyajikan empat kelompok. **01-web-utama/** berisi salinan mandiri kode dan aset asli, tanpa pintasan. Kelompok lainnya tetap berupa pintasan. Sumber utama tetap pada jalur semula agar GitHub dan alat pembangun tidak terganggu. Folder pengelompokan tidak ikut diunggah ke GitHub.

| Folder kelompok | Kegunaan |
| --- | --- |
| `01-web-utama/` | Paket web mandiri berisi salinan kode dan aset asli, tanpa pintasan |
| `02-pengembangan/` | Dokumentasi, sumber pembangun, pengujian, dan aset sumber; tidak semuanya dimuat oleh pemain, tetapi berguna untuk pengembangan |
| `03-preview-dan-referensi/` | Katalog aset, halaman contoh, pilihan gaya, dan aset alternatif yang tidak diperlukan untuk menjalankan game utama |
| `04-arsip-lokal/` | Paket ZIP lama, hasil screenshot/pengujian, arsip aset, dan checkout hosting lama |

`kelompok-lokal/DAFTAR-FILE.csv` mencatat kelompok per file. Pengelompokan ini adalah inventaris versi saat dibuat, bukan aturan otomatis untuk menghapus file di masa mendatang.

## Yang diperlukan web utama

- `index.html`, `find.html`, `puzzle.html`, `matching.html`, `results.html`.
- `manifest.webmanifest` untuk mode aplikasi di HP.
- Kode CSS/JavaScript dan `content/game-content.json` yang dipakai halaman-halaman tersebut.
- Ilustrasi Temukan Benda aktif, gambar master puzzle, benda untuk mencocokkan, dan UI yang dirujuk game.

Daftar aset utama mengacu pada paket runtime yang sudah diterbitkan, ditambah ikon mute terbaru. Beberapa aset latar juga digunakan sebagai sumber pembangun gambar master; tetap dipertahankan sebagai bagian paket kerja.

## Yang tidak dimuat dalam permainan utama

- `asset-catalog.html`, `asset-catalog-3d.html`, `find-layout-preview.html`, dan `style-options/`: katalog dan contoh/referensi.
- `tools/` dan `docs/`: alat dan dokumentasi; tetap diperlukan untuk pemeliharaan, bukan file sampah.
- `assets/` di luar latar aktif: banyak merupakan aset sumber versi awal. Sebagian dipakai alat pembangun katalog, jadi jangan langsung dihapus.
- `assets-3d/puzzles/separate/`: ekspor keping untuk katalog; game aktif memotong master menggunakan layout jigsaw.
- `output/`, `assets-archive/`, paket `*.zip`, dan `sites/`: keluaran lokal/arsip/salinan hosting. Bukan sumber utama GitHub/Vercel.

Tidak ada file asli yang dihapus atau dipindahkan. Tidak ada perubahan deploy pada tugas pengelompokan ini.

Panduan menambah gambar dan sesi: `docs/MENAMBAH-VARIASI-GAME.md`.
