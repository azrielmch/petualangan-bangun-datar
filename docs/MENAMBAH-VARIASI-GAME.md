# Menambah variasi gambar dan sesi game

Bisa. Jumlah level tetap lima per game; jumlah gambar, tema, dan pilihan benda pada setiap level bisa diperbanyak.

## Kondisi saat ini

| Game | Isi saat ini | Pengacakan |
| --- | --- | --- |
| Temukan Benda | 10 ilustrasi, dua gambar per bentuk | Gambar dipilih sesuai bentuk pada level; saat mengulang, menghindari gambar sebelumnya jika tersedia alternatif |
| Puzzle | 5 tema × 5 bentuk = 25 gambar master | Tema, bentuk, dan urutan kepingan dipilih acak; level tetap 4, 4, 6, 6, 8 keping |
| Mencocokkan | 40 benda untuk lima bentuk | Benda dipilih per bentuk dan posisi kartu kiri/kanan diacak; lima jenis pasangan tetap |

## Temukan Benda

1. Siapkan ilustrasi kartun 2.5D yang bersih, dengan benda menyatu dengan latar. Gunakan rasio 3:2, seperti gambar yang sudah ada.
2. Simpan gambar di `assets-3d/find-scenes-25d/`, dengan nama unik.
3. Daftarkan scene dan area klik tiap benda di `tools/build_find_scenes_25d.py`. Fungsi `S(...)` berisi identitas gambar, tema, dan bentuk target; `B(...)` berisi nama benda, bentuk, dan koordinat area klik dalam persen 0–100. Jika menambah tema baru, tambahkan pula nama temanya pada pemetaan di fungsi `S`.
4. Setiap gambar harus memiliki minimal tiga target yang masuk akal dan beberapa pengecoh. Pola sekarang menggunakan minimal lima pengecoh. Persegi dan persegi panjang perlu terlihat berbeda.
5. Jalankan pembangun scene, lalu pembangun konfigurasi game. Level otomatis mengambil semua scene dengan bentuk target yang sesuai.
6. Uji seluruh area klik pada gambar, termasuk setelah tampilan diperbesar atau diputar.

```sh
python3 tools/build_find_scenes_25d.py
python3 tools/build_game_content.py
node tools/check_find_scenes.js
node tools/check_game_content.js
```

Menambahkan PNG saja belum membuatnya tampil dalam pengacakan. Area klik dan pendaftaran scene juga diperlukan. File `content/find-scenes.json` dan `content/game-content.json` merupakan hasil pembangun; perubahan langsung pada JSON dapat tertimpa saat dibangun ulang.

## Puzzle Jigsaw

Cara yang sudah didukung adalah menambahkan **tema baru**:

1. Siapkan latar tema baru.
2. Tambahkan tema pada `THEMES` di `tools/build_game_content.py`. Lengkapi `POOLS` untuk kelima bentuk karena pembangun juga menghasilkan kumpulan benda per tema.
3. Pembangun menghasilkan gambar master untuk tiap kombinasi tema dan bentuk di `assets-3d/puzzles/themes/`, lalu mendaftarkannya dalam `content/game-content.json`.
4. Jalankan pemeriksaan puzzle dan konten.

```sh
python3 tools/build_game_content.py
node tools/check_puzzle_game.js
node tools/check_game_content.js
```

Papan game memotong gambar master saat dimainkan menggunakan pola jigsaw yang tersedia. Untuk mengekspor kembali katalog keping SVG terpisah, gunakan `tools/build_puzzle_playable.py`.

Saat ini pemilih puzzle memakai satu gambar untuk setiap kombinasi tema dan bentuk (`find` pada daftar variants di `content/randomizer.js`). Jika ingin beberapa gambar berbeda dalam **tema dan bentuk yang sama**, pemilih itu perlu diubah untuk mengambil salah satu gambar yang cocok secara acak. Menambahkan variant kedua dengan kombinasi yang sama saja belum cukup.

## Game Mencocokkan

1. Tambahkan ilustrasi benda dengan latar transparan ke `assets-3d/objects/`.
2. Daftarkan ID benda pada bentuk yang benar di `GROUPS` pada `tools/build_game_content.py`.
3. Tambahkan nama yang mudah dipahami anak pada `LABELS` bila diperlukan.
4. Bangun konfigurasi dan uji pasangan.

```sh
python3 tools/build_game_content.py
node tools/check_matching_game.js
node tools/check_game_content.js
```

Benda baru akan ikut dipilih secara acak di level 2, 3, dan 5. Level 1 dan 4 memakai bentuk dasar/nama/ciri-ciri sehingga variasinya terutama pada susunan kartu. Untuk variasi materi baru pada kedua level itu, bank teks atau bentuk perlu diperluas dengan aturan pendidikan yang sesuai.

## Setelah menambah variasi

- Buka semua game melalui server lokal dan periksa visual serta interaksi.
- Perbarui versi/cache URL pada pemuatan konfigurasi/aset bila dibutuhkan agar browser HP tidak memakai data lama.
- Commit dan push ke GitHub untuk memicu deployment Vercel, lalu periksa status deployment dan gambar di situs publik.
- Jangan menambah gambar hanya ke salinan hosting `sites/`; sumber utama ada di folder proyek ini.

Catatan: beberapa pembangun menjalankan ulang keluaran aset. Simpan perubahan di sumber pembangunnya agar perbaikan tetap ada setelah regenerasi.
