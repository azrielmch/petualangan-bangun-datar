# Petualangan Bangun Datar — paket web mandiri

Folder ini berisi file asli (salinan), tanpa pintasan. Semua kode dan aset permainan ada di dalam folder ini. Tidak memerlukan folder induk, akun, database, Node.js, atau proses build untuk menjalankan web.

## Jalankan lokal

Buka terminal di folder ini, lalu jalankan:

```sh
python3 -m http.server 4175 --bind 127.0.0.1
```

Buka http://127.0.0.1:4175/ di browser. Gunakan server HTTP; membuka index.html langsung lewat file:// dapat membuat pengambilan data JSON diblokir browser.

## Hosting

Unggah seluruh isi folder ini, dengan index.html berada di root hosting. Untuk Vercel pilih proyek statis tanpa build; gunakan folder ini sebagai root proyek. Pertahankan struktur content/, assets-3d/, dan assets/.

## Isi

- index.html: beranda
- find.html: Temukan Benda
- puzzle.html: Puzzle Jigsaw
- matching.html: Ayo Mencocokkan
- results.html: hasil permainan
- content/: kode, CSS, dan konfigurasi konten
- assets-3d/ dan assets/: aset yang diperlukan web
- manifest.webmanifest: dukungan aplikasi HP

Mode Guru memakai kode 1324. Progres tersimpan pada browser masing-masing pemain. Untuk iPhone tanpa bilah browser, gunakan Safari > Bagikan > Tambahkan ke Layar Utama.

Folder ini adalah sumber utama dan repositori GitHub. Riwayat Git, alat pembangun (tools/), dokumentasi (docs/), katalog dan aset sumber telah digabung ke folder ini. Commit dan push dilakukan langsung dari folder ini saat diminta menerbitkan. Arsip lama berada di ../../arsip-lokal/.

## Pembaruan Android dan akhir level

Fullscreen native dipanggil langsung melalui sentuhan tombol beranda. Jika browser menolak, ada pemberitahuan dan kesempatan mencoba ulang. Seusai level, papan hasil tetap terlihat selama satu detik sebelum popup. Menutup popup dengan X menampilkan panah kanan di papan untuk melanjutkan; setelah lima level, tombol mengarah ke hasil akhir.

Repositori GitHub: https://github.com/azrielmch/petualangan-bangun-datar
Situs utama: https://petualangan-bangun-datar.vercel.app/

Panduan pengembangan: docs/MENAMBAH-VARIASI-GAME.md.

## Aset WebP kualitas 85

Gambar game memakai WebP kualitas 85 dengan dimensi dan transparansi tetap. SVG yang berisi gambar raster juga memakai WebP tertanam. Ukuran assets-3d turun dari 310,6 MB setelah kompresi lossless menjadi sekitar 29,9 MB. File sebelum konversi disimpan lokal di ../../arsip-lokal/sebelum-webp85/ dan tidak perlu diunggah ke hosting. Banner berhasil dimuat secara lazy agar tidak berebut unduhan saat game dibuka. Rincian: docs/ASSET-WEBP85.json.
