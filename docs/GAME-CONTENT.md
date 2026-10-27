# Petualangan Bangun Datar — 15 level dan variasi tema

## Jumlah level

Tiga permainan masing-masing mempunyai lima level: total 15 level. Pemain bebas memilih permainan; progres level setiap permainan tetap terpisah. COMPLETED baru muncul setelah semua 15 level selesai. Penilaian tetap memakai total kesalahan seluruh permainan dan rumus skor sebelumnya.

| Level | Temukan Benda | Puzzle Jigsaw | Mencocokkan |
|---|---|---|---|
| 1 | Cari 3 benda persegi | 4 keping | Bentuk × nama bangun datar |
| 2 | Cari 3 benda lingkaran | 4 keping | Bentuk × benda |
| 3 | Cari 3 benda segitiga | 6 keping | Benda × nama bangun datar |
| 4 | Cari 3 benda persegi panjang | 6 keping | Bentuk × ciri-ciri |
| 5 | Cari 3 benda segi lima | 8 keping | Benda × ciri-ciri |

## Lima latar dan tema

Puzzle memakai Kamar Anak, Ruang Belajar, Dapur Ceria, Taman Bunga, dan Hutan Kastel. Temukan Benda memakai ilustrasi terpisah dalam lima kategori: kamar, ruang belajar, dapur, taman, dan ruang keluarga. Sepuluh ilustrasi Temukan Benda dibuat baru sebagai gambar utuh; lihat `FIND-SCENES.md`. Tidak memakai emoji.

Struktur data mendukung penambahan tema tanpa mengubah aturan level. Pustaka benda terpisah tetap memiliki pengelompokan tema; sesi Temukan Benda kini memakai daftar ilustrasi dan area klik tetap yang sesuai dengan bentuk target.

## Temukan Benda

Temukan Benda kini memakai sepuluh ilustrasi utuh, dua gambar untuk setiap bentuk. Benda benar dan pengecoh menyatu dengan gambar. Setiap gambar mempunyai sedikitnya tiga benda benar dan lima pengecoh, dengan area klik yang ditandai manual. Siswa mencari tiga benda benar yang berbeda. Rincian dan daftar gambar ada di `FIND-SCENES.md`.

Gambar sesi baru tidak langsung mengulang gambar sebelumnya pada level yang sama. Semua benda di satu gambar tetap pada posisi alaminya; variasi berasal dari gambar utuh yang berbeda. Benda benar diberi lingkaran hijau, pengecoh diberi lingkaran merah, dan jawaban benar tidak dihitung dua kali. Ilustrasi lama yang menempelkan sprite di atas latar sudah digantikan untuk permainan ini. Perpustakaan 40 benda terpisah tetap tersedia untuk Mencocokkan dan kebutuhan aset lainnya.

## Puzzle Jigsaw

Jumlah keping selalu mengikuti level: 4, 4, 6, 6, 8. Bentuk serta tema gambar diacak secara terpisah, sehingga ada 25 gambar utuh: lima bentuk × lima tema. Gambar memuat ilustrasi karakter bangun datar dan nama yang benar. Tema dan bentuk tidak langsung mengulang sesi sebelumnya.

Kelima level dapat memakai seluruh 25 gambar; kesulitannya ditentukan oleh jumlah potongan. Gunakan path kepingan dari template level untuk memotong gambar terpilih, kemudian acak posisi kepingan. Seluruh kepingan harus menutup satu gambar yang sama tanpa celah atau duplikasi. Path, posisi target, dan batas tampilan tersedia pada data layout.

Gambar `assets-3d/puzzles/master-*.svg` dan `piece-*.svg` adalah contoh susunan bawaan. Gambar bervariasi berada di `assets-3d/puzzles/themes/`; gambar tersebut dapat dipasangkan dengan template level mana pun. Jangan mengikat satu bentuk secara permanen pada satu tingkat kesulitan.

## Mencocokkan

Setiap level memiliki lima pasangan, satu untuk setiap bangun datar. Jenis pasangan mengikuti tabel. Jika level menggunakan benda, pilih satu benda acak per bentuk dari delapan contoh yang tersedia. Pilihan kiri dan kanan diacak terpisah, kemudian dibekukan selama sesi berlangsung. Kebenaran pasangan memakai ID bentuk, bukan posisi baris atau teks tampilan.

Ciri-ciri: persegi mempunyai empat sisi sama panjang dan empat sudut siku-siku; lingkaran satu sisi lengkung tanpa sudut; segitiga tiga sisi dan tiga sudut; persegi panjang empat sudut siku-siku, dua sisi panjang serta dua sisi pendek; segi lima lima sisi dan lima sudut.

## Integrasi dan penyimpanan

Ketiga permainan dapat dimainkan dari `index.html` atau katalog. Masing-masing memiliki lima level, dan halaman hasil akhir merangkum level yang selesai, kesalahan, skor, serta bintang. Baca `HOME-AND-RESULTS.md` untuk aturan penyimpanan dan penilaian. Penyelesaian level disimpan pada perangkat; sesi level yang belum selesai dimulai ulang saat halaman dibuka lagi.

## Asal ilustrasi

Latar dapur, taman, dan 15 benda tambahan dibuat dengan built-in imagegen. Berkas PNG disalin tanpa pengeditan raster. Gambar puzzle dibuat sebagai komposisi SVG mandiri menggunakan latar serta karakter 3D yang sudah ada, dengan nama bentuk berupa teks. Prompt subjek ada di `theme-background-prompts.json` dan `theme-object-prompts.json`; gaya dasar mengikuti `ART-DIRECTION-3D.md`.
