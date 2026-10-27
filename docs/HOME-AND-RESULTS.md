# Beranda dan hasil akhir

`index.html` adalah pintu masuk utama. Tiga kartu membuka Temukan Benda, Puzzle Bangun Datar, dan Ayo Mencocokkan. Menu bawah berisi Petunjuk, Hasil Akhir, serta Pengaturan suara. Logo menggunakan aset asli; latar petualang dan papan hasil dibuat melalui built-in imagegen. Teks, tombol, skor, bintang, dan tabel merupakan elemen antarmuka terpisah.

`results.html` menampilkan ringkasan tiga permainan. `results.html?game=find`, `?game=puzzle`, atau `?game=matching` menampilkan hasil permainan tersebut. Jika belum selesai lima level, halaman menampilkan kemajuan dan tombol lanjut, bukan status Completed atau skor 100.

## Alur dan progres

`content/game-progress.js` menyimpan level yang selesai di localStorage dengan kunci `bangun-datar-progress-v1`. Setiap game mempunyai putaran terpisah. Setiap level dicatat satu kali pada penyelesaian pertama dalam putaran itu; bermain ulang level yang sama tidak menggandakan catatan atau mengubah skor yang tersimpan. Tombol Main Lagi di hasil akhir memulai putaran baru hanya untuk game tersebut. Preferensi suara disimpan terpisah dalam catatan yang sama.

Beranda melanjutkan dari level pertama yang belum selesai. Yang disimpan adalah penyelesaian level, bukan posisi setiap benda atau keping di level yang sedang berjalan; level yang belum selesai dimulai sebagai sesi baru saat halaman dibuka lagi. Menyelesaikan level lima saja tidak dianggap menyelesaikan kelima level.

`content/game-page.js` menghubungkan ketiga halaman permainan ke pencatatan hasil. Setelah semua level selesai, tombol lanjut berubah menjadi Lihat Hasil Akhir. Katalog juga mencatat penyelesaian dan mengarah ke hasil akhir jika seluruh level game selesai. Tombol kembali pada layar game mengarah ke beranda.

## Nilai

Kesalahan adalah jumlah jawaban/drop salah pada lima sesi level yang tercatat. Skor mengikuti rancangan sebelumnya: `max(0, 100 - 10 × ceil(kesalahan / 5))`. Tanpa kesalahan mendapat 100; 1–5 kesalahan mendapat 90; 6–10 mendapat 80. Bintang adalah skor dibagi 20, termasuk setengah bintang. Skor akhir hanya ditampilkan setelah lima level selesai. Tabel menampilkan status dan kesalahan setiap level.

## Verifikasi

`node tools/check_game_progress.js` memeriksa tiga game, lima level wajib, batas skor dan bintang, tidak ada pencatatan ganda, penyimpanan, suara, serta Main Lagi yang tidak menghapus game lain. Pengujian browser memakai asal lokal terpisah agar tidak mengubah progres pengguna. Semua lima level untuk tiga game diselesaikan melalui UI: 15 level, 28 keping puzzle, 25 pasangan, dan 15 target Temukan Benda. Uji satu kesalahan nyata pada Mencocokkan menghasilkan skor 90 dan 4,5 bintang.

## Revisi kucing, ikon, dan pop-up level

Anjing diganti kucing oranye-putih pada beranda dan hasil akhir. Halaman hasil memakai petualang berdiri, banner Completed yang lebih kecil, dan ruang tabel lebih jelas. Aset lama diarsipkan di `assets-archive/home-results-before-cat/`. Prompt edit ada di `cat-home-results-prompts.json`.

Enam ikon tombol beranda memakai SVG berwarna, gradasi volume lembut, dan bayangan yang mengikuti sistem UI. Sumber pembangunnya `tools/build_home_icons.py`.

Penyelesaian level pada ketiga permainan kini membuka dialog modal native melalui `content/level-celebration.js` dan CSS pasangannya. Banner GREAT/Completed serta tombol lanjut berada di dalam pop-up. Tombol tutup atau Escape memungkinkan melihat papan lagi, dan tombol Lihat Hasil Level membuka pop-up kembali. Setelah seluruh lima level tercatat, tombol di pop-up membuka hasil akhir. Pencatatan skor dan kesalahan tetap memakai aturan sebelumnya. Tutup/buka ulang, perpindahan level, dan tautan hasil diuji melalui browser pada ketiga game.

## Kucing abu-abu dan tombol satu bingkai

Revisi terbaru memakai kucing tabby abu-abu dengan bagian putih pada beranda dan hasil akhir. Gambar kucing oranye dipindahkan ke `assets-archive/home-results-orange-cat/`. Completed di hasil akhir memakai `completed-text-only.png`, huruf emas transparan tanpa papan, daun, bintang, atau ornamen. Banner dekoratif pada pop-up selesai level tetap menggunakan aset yang sebelumnya disetujui.

Tombol beranda, hasil, dan aksi lanjut pada pop-up menggunakan satu gambar bingkai kayu, tanpa border CSS luar, latar solid, atau lapisan kotak tambahan. Jarak tombol serta posisi judul hasil disesuaikan mengikuti referensi terbaru. Prompt edit raster dibuat lewat built-in imagegen dan disimpan di `gray-cat-clean-results-prompts.json`.
