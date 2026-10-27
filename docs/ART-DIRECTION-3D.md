# Petualangan Bangun Datar — Arah visual versi 3D

Versi ini menggantikan arah ilustrasi datar pada karakter dan benda. Aset versi sebelumnya tetap disimpan di `assets/`; versi baru berada di `assets-3d/`. Tiga latar lama dipakai kembali karena sudah mempunyai tekstur, volume, dan pencahayaan yang sesuai.

Pembaruan isi permainan: lihat `GAME-CONTENT.md` untuk 15 level, lima tema, 40 benda, 25 gambar puzzle bertema, serta pengacakan sesi. Tingkat kesulitan puzzle tetap 4, 4, 6, 6, dan 8 keping.

Pembaruan Temukan Benda: lihat `FIND-SCENES.md`. Permainan ini sekarang memakai 10 ilustrasi utuh dengan benda menyatu, area klik manual, lingkaran hijau/merah, dan misi mencari tiga benda. Aset benda transparan tetap dipakai untuk keperluan lain.

Gaya aktif Temukan Benda mengikuti pilihan pengguna **Kartun 2.5D clean**, bukan versi realistis sebelumnya. Sepuluh ilustrasi terbaru ada di `assets-3d/find-scenes-25d/`; panduan khusus dan pembedaan persegi/persegi panjang ada di `FIND-SCENES-25D.md`.

## Bahasa visual

Kartun 3D lembut dengan sentuhan lukisan tangan, tepi membulat, sorotan lebar, tekstur bahan, bayangan kontak cokelat hangat, dan cahaya keemasan dari kiri atas. Hindari garis hitam tebal dan bidang warna rata. Setiap benda tetap digambar dari depan atau atas; kedalaman hanya tipis agar siluet bangun datar terbaca jelas.

Persegi biru langit, lingkaran merah muda koral, segitiga kuning keemasan, persegi panjang hijau daun, segi lima ungu lavender. Karakter memiliki mata gelap berkilau, pipi merah muda, dan ekspresi ramah. Pose perayaan memakai tangan ilustrasi khusus yang mengacungkan jempol. Tidak memakai emoji atau ikon font.

## Berkas

- `characters/*.png`: karakter 3D transparan dalam pose biasa dan perayaan.
- `objects/*.png`: 25 ilustrasi benda 3D transparan. Pakai alpha gambar sebagai acuan area klik; margin transparan bukan jawaban.
- `ui/*.svg`: simbol dan panel native yang diberi gradasi bahan, efek timbul, serta bayangan. Logo dan empat banner mempunyai pembungkus SVG mandiri dengan ilustrasi PNG tertanam.
- `ui/*.png`: bahan panel dan tombol 3D hasil imagegen.
- `puzzles/master-*.svg`: gambar utuh yang menanamkan karakter PNG 3D dan nama bentuk secara mandiri.
- `puzzles/piece-*.svg`: jumlah potongan meningkat sesuai level, dari empat sampai delapan. Menggunakan clipping SVG, tanpa mengubah PNG sumber.
- `puzzles/assembled-*.svg`: pratinjau gambar dengan seluruh garis sambungan.
- `puzzles/layout-*.json`: posisi, path, dan batas tampilan kepingan pada setiap level. `jigsaw-layout.json` berisi seluruh level.
- `manifest.json`: indeks file beserta ukuran aktualnya.

PNG disalin tanpa pengeditan dari keluaran built-in imagegen. SVG dan gambar raster adalah aset 2D bergaya 3D, bukan model 3D yang dapat diputar. Efek audio tetap dibuat pada tahap implementasi menggunakan Web Audio API.

## Integrasi

Katalog menampilkan contoh komposisi objek di kamar, karakter, benda, puzzle, dan antarmuka. Contoh komposisi hanya untuk pemeriksaan visual, bukan gameplay. Saat implementasi, pertahankan rasio objek, cocokkan skala berdasarkan benda di ruangan, dan gunakan bayangan ringan yang sama. Jangan menggelapkan gambar dengan bayangan ganda yang berlebihan.

Jendela dipertahankan sebagai satu bidang persegi tanpa kisi pembagi. Koin dan lingkaran berupa cakram tipis, bukan bola. Segi lima harus selalu memiliki tepat lima sisi. Untuk bentuk persegi panjang, panjang dan lebar terlihat berbeda. Dekorasi pada latar tidak otomatis menjadi objek yang dapat diklik.

## Peningkatan kesulitan puzzle

| Level | Bentuk | Jumlah keping | Susunan |
|---|---|---:|---|
| 1 | Segitiga | 4 | 2 × 2 |
| 2 | Persegi | 4 | 2 × 2 |
| 3 | Lingkaran | 6 | 3 × 2 |
| 4 | Persegi panjang | 6 | 3 × 2 |
| 5 | Segi lima | 8 | 4 × 2 |

Total 28 keping. Semua kepingan memiliki tonjolan/lekukan yang saling cocok, tanpa area gambar yang kosong atau terduplikasi. Ukuran papan tetap 480 × 360. Koordinat path memakai ruang papan; `bounds` adalah batas tampilan konservatif untuk memuat tonjolan, bukan area jawaban. Gunakan path untuk hit testing.

Saat game diimplementasikan, indikator dan syarat selesai membaca `pieceCount` dari layout level, bukan angka tetap enam. Penghitung awal berturut-turut 0/4, 0/4, 0/6, 0/6, dan 0/8. Semua keping level harus terkunci pada posisi benar sebelum GREAT muncul. Aturan skor dan kesalahan tetap mengikuti rancangan sebelumnya. Paket ini masih berupa aset, belum mekanisme permainan.

## Prompt dasar produksi

“Create ONE isolated production sprite on genuine TRANSPARENT background. Style: premium 3D cartoon child's educational adventure mobile game, softly rounded shallow bevels, rich hand-painted material textures, upper-left warm golden sunlight, soft highlights, honey-brown ambient occlusion and subtle edge shading. Match cozy golden wooden room backgrounds. FRONT or exact TOP view, mathematically clear flat outer silhouette with shallow thickness only. No perspective tilt, no black outlines, no thick vector strokes, no flat vector art, no emoji, no lettering, no watermarks, no floor or scene, no other objects. One centered object with generous transparent padding.”

Untuk karakter: tambahkan bahan satin lembut, mata gelap berkilau, pipi merah muda, dan mulut tersenyum. Untuk pose GREAT: tambahkan satu lengan pendek dan tangan krem yang mengacungkan jempol, tanpa mengubah bentuk dasar.

Untuk panel: bingkai kayu madu bertekstur dengan sudut membulat dan bagian tengah krem kosong. Untuk tombol: bidang lingkaran jingga keemasan dengan rim timbul dan tengah kosong untuk simbol native.

## Pembaruan logo dan banner

Lima aset dibuat ulang melalui built-in imagegen: `logo.png`, `banner-completed.png`, `banner-correct.png`, `banner-great.png`, dan `banner-wrong.png`. Kelimanya memakai papan kayu bertekstur, tepi timbul, cahaya hangat kiri atas, dan tipografi 3D. Manifest menunjuk PNG sebagai versi utama; SVG dengan nama yang sama tetap tersedia untuk kompatibilitas. Teks yang dipakai persis: Petualangan Bangun Datar, COMPLETED, BENAR, GREAT!, dan COBA LAGI, YA!.

COMPLETED dan GREAT memakai aksen emas, BENAR hijau daun, COBA LAGI, YA! koral lembut. Logo memakai judul kuning keemasan dan biru turquoise, disertai lima bentuk kecil tanpa wajah. Tidak memakai emoji. Prompt subjek disertakan di `docs/3d-ui-prompts.json`.

Daftar subjek benda mengikuti metadata paket: jendela, bingkai, ubin, serbet, catatan; koin, piring, jam, kancing, biskuit bulat; pizza, penggaris, bendera, roti, rambu; pintu, buku, karpet, papan, tempat pensil; biskuit segi lima, bingkai segi lima, lencana, ubin segi lima, papan segi lima.
