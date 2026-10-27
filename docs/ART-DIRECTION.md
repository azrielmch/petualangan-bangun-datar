# Petualangan Bangun Datar — Panduan aset

Paket aset untuk tiga permainan kelas 2 SD. Tidak memakai emoji, ikon font, stok eksternal, atau gambar bangun ruang sebagai jawaban.

## Gaya

Kartun petualangan anak, garis tepi cokelat hangat, bentuk membulat, pencahayaan keemasan, kayu madu, tanaman hijau, dan bidang krem. Latar memakai ilustrasi raster bertekstur; objek interaktif memakai SVG yang lebih sederhana dan tegas agar mudah dikenali pada layar kecil. Benda digambar tampak depan/atas agar siluet bangun datarnya jelas.

Palet: garis #69402c; krem #fff4d8; persegi #43bdf0; lingkaran #f27d9e; segitiga #ffd15d; persegi panjang #8dc943; segi lima #b887e8. Warna bentuk sama pada karakter, ikon, dan puzzle. Benda nyata boleh mengikuti warna materialnya.

## Pemakaian

- `backgrounds/forest-castle.png`: beranda, peta, dan perayaan akhir; gunakan panel krem untuk keterbacaan teks.
- `backgrounds/child-room.png`: latar Temukan Benda. Benda jawaban ditambahkan sebagai lapisan terpisah. Dekorasi yang sudah menyatu dengan latar bukan objek jawaban; petunjuk perlu menjelaskan objek interaktif.
- `backgrounds/workshop.png`: latar Puzzle dan Mencocokkan.
- `characters/`: lima karakter, masing-masing pose biasa dan pose gembira dengan tangan mengacungkan jempol yang digambar khusus.
- `objects/`: 25 benda, masing-masing lima contoh untuk setiap bentuk. Pengulangan bentuk dalam bingkai tidak dihitung sebagai benda tambahan.
- `puzzles/master-*.svg`: lima gambar utuh dengan nama bentuk.
- `puzzles/piece-*.svg`: 30 keping nyata, enam per bentuk. Semua memakai viewBox papan 480 × 360. Saat diintegrasikan, potong area tampilan sesuai bounding box setiap path; koordinat target ada di jigsaw-layout.json. Jangan gunakan seluruh persegi pembatas sebagai area penilaian.
- `puzzles/jigsaw-outline.svg`: garis pemisah untuk bantuan dan pratinjau.
- `ui/`: logo, panel, tombol, ikon, kartu pasangan, thumbnail menu, simpul peta, banner, dan tiga keadaan bintang.

SVG karakter/benda memakai latar transparan. Logo dan banner mengandung teks; instruksi dan skor permainan harus tetap berupa teks HTML. Font menggunakan Trebuchet MS dengan Arial sebagai fallback sistem.

## Aturan integrasi

Ukuran sentuh minimum 48 px. Area klik harus mengikuti siluet benda atau path puzzle; bukan semua area transparan. Pertahankan rasio gambar. Tambahkan label aksesibilitas melalui HTML. Tampilkan teks dan simbol untuk umpan balik, jangan hanya mengandalkan warna. Lingkaran hijau jawaban dibuat melalui SVG/CSS dan diposisikan berdasarkan objek.

Setiap level Temukan Benda memiliki lima benda benar dengan target empat, ditambah pengecoh. Daftar penempatan dan logika penilaian disusun saat pembuatan permainan, bukan dibakar ke latar.

Efek suara dibuat pada tahap implementasi memakai Web Audio API, tanpa file audio. Nada benar, buzzer salah lembut, kemenangan berurutan; harus tunduk pada tombol senyap.

## Asal dan prompt ilustrasi

Tiga latar dibuat memakai built-in imagegen; aset SVG dibuat khusus secara deterministik. Tidak ada raster yang diedit atau dipotong dengan skrip.

Prompt dasar: “Production landscape game background, 1536x1024. Polished hand-painted 2D children's adventure cartoon, thick soft dark-brown contours, rounded forms, warm golden sunlight, honey oak wood, leafy jade and mint plants, cream and turquoise with coral and violet accents. Clear central area for separate interactive game layers. No text, letters, numbers, emoji, watermark, UI, or buttons.”

Prompt hutan: “A winding path through lush friendly forest toward a small whimsical castle in far background, framing foliage and flowers, open bright central clearing. Detailed edges and calm low-detail center. No characters.”

Prompt kamar: “Cozy child's room, straight-on camera, bookcase at left edge, bed at right edge, curtains and distant garden view, warm wooden floor and low neutral rug. Large uncluttered wall and floor in middle for separate clickable objects. No loose toys, balls, gift boxes, people. Avoid dramatic perspective.”

Prompt bengkel: “Cozy school art corner with colorful books and pencils at far left edge, potted plant at far right edge, softly lit window upper edge, broad empty warm cream and wood display area occupying central 80 percent for separate UI and puzzle pieces. Framing props only. No characters or shapes to solve.”

## Batas paket

Katalog adalah pratinjau aset, belum aplikasi permainan. Drag-and-drop, skor, simpan progres, navigasi, animasi, dan audio akan diimplementasikan saat pengembangan game. Ilustrasi raster tetap perlu pengujian komposisi pada ukuran HP saat diintegrasikan.
