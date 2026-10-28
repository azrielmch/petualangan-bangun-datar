# Puzzle Biru Ceria

Buka `puzzle.html` atau pilih Puzzle di katalog sesi acak. Lima level memakai 4, 4, 6, 6, 8 keping. Tersedia 25 variasi gambar (lima tema × lima bentuk), menggunakan karakter 3D yang sudah ada. Nama bentuk tampil pada panel level dengan huruf membulat; judul menggunakan gambar huruf timbul Biru Ceria.

Papan kiri kosong tanpa panduan, bayangan gambar, atau garis slot. Keping kanan berupa elemen SVG terpisah, diacak setiap sesi dan tetap tegak. Keping yang diletakkan dekat posisi benar menempel dan terkunci; posisi salah mengembalikan keping ke baki. Penghitung tidak menggandakan keping terpasang. Semua keping selesai menampilkan banner Completed dan tombol lanjut. Mouse dan sentuhan memakai Pointer Events. Alternatif: pilih keping lalu klik papan, atau gunakan panah dan Enter. Tombol suara mengaktifkan bunyi jawaban benar.

`assets-3d/ui/puzzle-biru-shell.webp` adalah latar antarmuka kosong hasil built-in imagegen. Keping tidak dibakar ke gambar itu. Ilustrasi master `assets-3d/puzzles/themes/` dirakit dari aset latar dan karakter yang ada. `content/puzzle-pieces.json` berisi 700 keping SVG terpisah untuk 25 variasi × seluruh lima level; SVG menggunakan referensi relatif ke master, sehingga struktur folder harus dipertahankan.

Jalankan `tools/build_game_content.py`, `tools/build_3d_catalog.py`, dan `tools/build_puzzle_playable.py` saat membangun ulang. Verifikasi interaksi: `node tools/check_puzzle_game.js`. Tidak ada rotasi keping yang diwajibkan.
