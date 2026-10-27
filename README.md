# Petualangan Bangun Datar

Buka beranda `index.html` melalui server web lokal atau hosting statis. Semua game dan hasil berjalan di browser, tanpa layanan akun atau database.

Untuk menjalankan lokal dari folder ini:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Kemudian buka `http://127.0.0.1:4173/`.

- Temukan Benda: lima level, sepuluh ilustrasi, gambar utuh di dalam bingkai.
- Puzzle: lima level dengan 4, 4, 6, 6, dan 8 keping terpisah.
- Mencocokkan: lima jenis pasangan sesuai tingkatnya.
- Beranda: petualang bersama kucing, ikon tombol berwarna, petunjuk, pengaturan suara/Mode Guru, dan rangkuman hasil.
- Saat masuk game: dialog petunjuk dengan tombol Mulai; level dan sesi baru hanya tampil jika Mode Guru aktif.
- Layar penuh: tombol hanya di beranda dan mencakup seluruh aplikasi, termasuk dialog dan hasil. Di iPhone, tambahkan situs ke Layar Utama melalui Safari untuk membuka tanpa bilah browser.
- Selesai level: pop-up GREAT/Completed dengan tombol lanjut dan pilihan melihat papan lagi.
- Hasil akhir: karakter berdiri, status lima level, kesalahan, skor, dan bintang untuk setiap game.

Progres level yang sudah selesai tersimpan pada browser di perangkat ini. Lihat `docs/HOME-AND-RESULTS.md` untuk rincian perilaku dan penilaian. Katalog aset tersedia di `asset-catalog.html`.

Situs publik: https://petualangan-bangun-datar.sharpelf14.chatgpt.site

Mode Guru meminta kode `1324` untuk menampilkan pemilihan level dan gambar/sesi baru. Kode ini adalah pengunci antarmuka lokal, bukan autentikasi server. Efek suara mengikuti pengaturan suara dan aktif setelah pengguna menyentuh layar.

Pemeriksaan game:

```sh
node tools/check_game_progress.js
node tools/check_find_scenes.js
node tools/check_puzzle_game.js
node tools/check_matching_game.js
```

Pembaruan akhir level: dialog berhasil muncul setelah satu detik agar papan yang selesai dapat terlihat. Menutup dialog dengan X menampilkan panah kanan untuk melanjutkan level atau melihat hasil akhir. Pemanggilan fullscreen dari beranda memakai interaksi tombol secara langsung; jika ditolak browser, petunjuk ditampilkan.
