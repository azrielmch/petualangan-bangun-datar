# Ayo Mencocokkan · Biru Ceria

Game tersedia di `matching.html` dan pilihan Mencocokkan pada katalog sesi acak. Layout mengikuti referensi pengguna: judul serta petunjuk di atas, lima kartu kiri dengan bingkai merah muda, lima kartu kanan dengan bingkai biru, titik sambungan di sisi dalam, dan ruang tengah untuk garis penghubung. Bahan kayu, panel krem, banner biru toska, dan judul kuning timbul mengikuti game Puzzle Biru Ceria.

Lima level:
1. Bentuk bangun datar × nama bangun datar.
2. Bentuk bangun datar × benda dengan bentuk tersebut.
3. Benda × nama bangun datar.
4. Bangun datar × ciri-ciri.
5. Benda × ciri-ciri bentuknya.

Setiap level mempunyai lima pasangan. Urutan kedua kolom diacak; benda dipilih ulang pada sesi berikutnya dan tidak langsung mengulang benda yang sama untuk tiap bentuk. Jawaban diperiksa berdasarkan bentuk, bukan urutan posisi.

Pemain bisa menarik garis dari salah satu sisi ke sisi lain, mengetuk dua kartu, atau memilih dengan Tab dan Enter/Spasi. Pasangan benar mendapat garis hijau dan terkunci, pasangan salah bergaris merah putus-putus dan bisa dicoba kembali. Pemilihan berikutnya menghapus garis salah. Selesai lima pasangan menampilkan Completed dan tombol lanjut; level lima mengarah kembali ke level satu. Tombol suara dapat diaktifkan/dimatikan.

Latar `assets-3d/ui/matching-biru-shell.webp` dibuat dengan built-in imagegen dan tidak berisi kartu atau garis yang dibakar ke gambar. Kartu, titik, teks, dan garis berupa elemen SVG terpisah. Bentuk serta benda memakai aset yang sudah tersedia. Prompt gambar ada di `matching-shell-prompt.json`.

Validasi: `node tools/check_matching_game.js` menguji 250 sesi pada lima mode, jawaban salah, mencoba kembali, penguncian pasangan, penyelesaian, dan pergantian benda. Interaksi menarik garis, mengetuk, dan lanjut level juga diperiksa di browser.

Teks ciri-ciri diringkas menjadi tepat dua baris pada level 4 dan 5. Pemisah baris disimpan dalam data agar tidak bergantung pada pembungkusan teks otomatis.
