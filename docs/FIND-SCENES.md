# Temukan Benda — ilustrasi utuh dan area klik

Versi ini menggantikan penyusunan sprite terpisah di atas latar untuk Temukan Benda. Setiap PNG adalah satu ilustrasi utuh; target dan pengecoh sudah dilukis di dalam ruangan atau taman dengan perspektif, permukaan, dan bayangan yang sesuai. Tidak ada benda jawaban yang dipindah atau ditempel sebagai lapisan gambar terpisah.

Gaya aktif adalah Kartun 2.5D clean yang dipilih pengguna. Lihat `FIND-SCENES-25D.md`. Ilustrasi yang lebih realistis sebelumnya sudah diarsipkan.

## Lima level, sepuluh gambar

| Level | Bentuk | Variasi gambar |
|---|---|---|
| 1 | Persegi | Kamar Baca, Kelas Ceria |
| 2 | Lingkaran | Dapur Sarapan, Ruang Keluarga |
| 3 | Segitiga | Taman Piknik, Ruang Bermain |
| 4 | Persegi panjang | Kamar Tidur, Dapur Hangat |
| 5 | Segi lima | Taman Bunga, Ruang Santai |

Setiap gambar mempunyai sedikitnya tiga benda target yang telah diperiksa secara visual dan sedikitnya lima pengecoh. Kamar Tidur juga menyediakan bantal putih memanjang sebagai jawaban benar tambahan. Misi setiap sesi adalah menemukan tiga benda benar yang berbeda. Benda tampak dari depan atau atas agar bentuknya terbaca; bola, kubus, dan piramida tidak digunakan sebagai target.

Saat membuka sesi baru, pilih gambar yang sesuai dengan bentuk pada level, tanpa langsung mengulang gambar sesi sebelumnya. Karena benda menyatu dengan ilustrasi, posisi dan isi benda pada satu gambar tetap. Variasi isi berasal dari pemilihan ilustrasi yang berbeda, bukan mengacak posisi sprite di atas gambar.

## Jawaban dan lingkaran

- Benda benar diberi lingkaran hijau dan penghitung bertambah satu.
- Benda pengecoh diberi lingkaran merah dan penghitung kesalahan bertambah satu.
- Benda yang sudah ditemukan tidak dihitung dua kali dan tidak menambah kesalahan.
- Klik ulang pada pengecoh menambah satu kesalahan per jawaban, tetapi tidak menggandakan lingkarannya.
- Klik pada latar yang bukan area benda tidak dihitung sebagai kesalahan.
- Setelah 3/3, level selesai dan GREAT! muncul. Pilihan lanjut membuka level berikutnya.

Area klik tidak ditampilkan sebelum dijawab. Lingkaran mengikuti letak benda, bukan letak klik pengguna. Area klik poligon dipakai untuk beberapa benda bersudut; area elips dipakai untuk benda lain. Semua koordinat berupa persentase dari gambar asli. Gambar selalu ditampilkan utuh tanpa pemotongan sehingga area klik tetap sejajar pada komputer maupun HP.

## Berkas

- `assets-3d/find-scenes-25d/*.png`: 10 ilustrasi dari built-in imagegen, termasuk revisi bentuk melalui imagegen.
- `content/find-scenes.json`: 81 benda yang ditandai manual, bentuk jawaban, area klik, dan ukuran asli gambar.
- `content/find-game.js` dan `find-game.css`: interaksi klik/tap, dukungan keyboard, lingkaran, penghitung, dan hasil level.
- `tools/build_find_scenes_25d.py`: sumber koordinat untuk pemeliharaan; dipanggil melalui `tools/build_find_scenes.py`.
- `docs/clean-25d-find-prompts.json`: subjek, referensi gaya, dan komposisi yang digunakan untuk imagegen.

Gaya prompt bersama: satu ilustrasi permainan mencari benda yang koheren, kartun buku cerita dengan volume 3D dan tekstur hangat, kayu madu, cahaya keemasan kiri atas, tanaman hijau, semua benda berada pada permukaan atau terpasang secara wajar. Hindari benda melayang, susunan grid, kartu ikon terpisah, emoji, antarmuka yang tercetak, tanda jawaban, dan lingkaran yang dilukis ke PNG. Jumlah dan bentuk target disebutkan secara terpisah untuk setiap gambar.

Perubahan ini hanya menjadikan Temukan Benda dapat dimainkan di katalog. Puzzle dan Mencocokkan tetap mengikuti data level sebelumnya dan masih berupa pratinjau materi. Perhitungan skor seluruh 15 level, penyimpanan progres bermain lengkap, dan audio seluruh permainan belum menjadi bagian dari katalog ini.
