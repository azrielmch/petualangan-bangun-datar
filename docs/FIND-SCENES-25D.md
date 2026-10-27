# Temukan Benda — Kartun 2.5D yang dipilih

Gaya final mengikuti pilihan 2 dari contoh sekolah: `style-options/school-02-soft-25d.png`. Sepuluh ilustrasi dibuat ulang melalui built-in imagegen menggunakan gambar tersebut sebagai referensi gaya. Hasil PNG disimpan tanpa pengeditan raster di `assets-3d/find-scenes-25d/`.

Gaya menggunakan volume dan bayangan lembut, permukaan matte, warna hangat, tekstur kayu sangat ringan, serta sedikit dekorasi. Tema sekolah hadir pada gambar kelas dan ruang belajar. Benda tetap menjadi bagian dari satu ilustrasi yang koheren, bukan sprite yang melayang di atas latar.

Revisi kewajaran benda pada tema sekolah: bantal merah di kursi dihapus dan diganti papan gabus persegi yang terpasang di dinding; piring pada meja kelas diganti penghapus; rebana di ruang belajar diganti tempat pensil. Papan gabus menjadi jawaban benar untuk persegi. Penghapus dan tempat pensil menjadi pengecoh sesuai permintaan bentuk pada levelnya. Area klik lama dihapus dan diganti mengikuti letak benda baru. Prompt edit ada di `school-realism-prompts.json`.

## Persegi dan persegi panjang

Revisi kelas terbaru menghapus sandaran kursi di belakang meja. Buku biru dibuat lebih tipis dan memanjang dengan sampul persegi panjang yang terlihat jelas. Area klik buku mengikuti ilustrasi terbaru. Prompt tersimpan di `classroom-chair-book-prompts.json`.

- Persegi mempunyai empat sisi sama panjang; wajah benda dibuat mendekati rasio 1:1 dan menghadap depan agar tidak tampak memanjang karena perspektif.
- Persegi panjang mempunyai sisi panjang dan sisi pendek yang jelas berbeda. Contoh buku, remot, bingkai memanjang, dan alas makan memakai proporsi memanjang sekitar 2:1 atau lebih.
- Buku tidak digunakan sebagai contoh persegi. Target persegi memakai jendela, papan, bingkai, atau bantal yang terlihat sama lebar dan tingginya.
- Target dan pengecoh diperiksa pada gambar hasil akhir. Area klik diperbarui mengikuti posisi ilustrasi baru.
- Jika siswa memilih persegi panjang saat diminta persegi, atau sebaliknya, pesan salah menjelaskan perbedaan panjang sisinya.

## Permainan

Lima level, masing-masing dua variasi ilustrasi. Setiap gambar mempunyai sedikitnya tiga benda benar dan beberapa pengecoh. Gambar sesi baru tidak langsung mengulang gambar sebelumnya. Lingkaran hijau menandai benar, merah menandai salah. Penghitung jawaban benar tidak bertambah saat benda yang sama diklik lagi. Setelah tiga jawaban benar, GREAT muncul dan pemain dapat melanjutkan.

Data aktif ada di `content/find-scenes.json`, dan sumber koordinat di `tools/build_find_scenes.py`. Ilustrasi sebelumnya dipertahankan dalam arsip terpisah. Prompt lengkap untuk revisi ini tersedia di `docs/clean-25d-find-prompts.json`.

## Bingkai Biru Ceria untuk seluruh level

Sepuluh gambar pada lima level kini memakai bingkai yang disetujui pada contoh kelas. Buka `find.html` atau pilih Temukan Benda pada katalog. Ikon bentuk, petunjuk, level, penghitung, dan panel potongan benda ditemukan menyesuaikan sesi. Gambar baru memilih variasi lain pada level yang sama; tombol lanjut membuka level berikutnya. Ilustrasi tetap utuh tanpa dipotong dan area klik tetap mengikuti gambar. Komponen layout ada di `content/find-frame-game.js` dan `content/find-frame.css`. Seluruh sepuluh gambar diperiksa sampai selesai 3/3 di browser.

Beranda utama tersedia di `index.html`. Setelah lima level selesai, tombol Lihat Hasil Akhir membuka ringkasan permainan. Detail progres dan nilai ada di `HOME-AND-RESULTS.md`.
