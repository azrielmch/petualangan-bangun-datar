# Perbaikan lokal: Mode Guru, dialog Mulai, dan layar HP

Perubahan ini diterapkan pada workspace lokal. Checkout dan versi publik Sites tidak diperbarui pada tahap ini.

## Tampilan anak dan guru

Mode Guru tersedia di Beranda → Pengaturan dan mati secara default. Preferensi disimpan bersama pengaturan suara tanpa mengubah progres. Saat mati, bar Beranda/Level/Gambar Baru/Sesi Baru dan nama tema di atas ketiga game disembunyikan. Saat aktif, bar kembali muncul. Perubahan antar-tab juga diterapkan melalui storage event. Level yang selesai dan tombol lanjut tetap berfungsi pada mode anak.

Footer teks beranda dihapus. Petunjuk awal ketiga game tampil pada dialog modal dengan tombol Mulai, satu kali setiap membuka halaman game, bukan setiap lanjut level. Dialog memblokir interaksi dengan papan sampai Mulai ditekan. Petunjuk tidak lagi menambah footer visual di bawah game. Status benar/salah tetap menjadi live region untuk pembaca layar, sedangkan lingkaran dan garis jawaban tetap terlihat pada papan.

Penghitung Mencocokkan dan label level/penghitung Puzzle memakai kotak posisi yang terpusat di area krem pada gambar frame. Teks panjang Persegi Panjang mempunyai ukuran khusus agar tetap di dalam frame.

## Fullscreen dan landscape

Tombol Layar Penuh tersedia di beranda, tiga game, dan halaman hasil. Dialog awal juga menyediakan tombol ini agar permintaan fullscreen terjadi lewat interaksi pengguna. Kode mencoba Fullscreen API, kemudian screen.orientation.lock('landscape') jika tersedia. Jika tidak didukung atau dibatasi, mode layar luas memakai viewport tersedia dan memutar kanvas lewat CSS saat HP masih portrait. Keluar layar penuh atau Escape mengembalikan layout normal. Frame tetap memakai rasio 3:2, tidak dipotong; ruang tersisa menjadi letterbox.

Ukuran kanvas mengikuti viewport dinamis dan tinggi kontrol guru. Perhitungan menggunakan tinggi layout toolbar yang tidak terpengaruh rotasi. Posisi klik/drag SVG tetap memakai transformasi koordinat browser. Native dialog mempertahankan navigasi keyboard dan tombol Mulai.

Referensi dukungan API: https://developer.mozilla.org/en-US/docs/Web/API/ScreenOrientation/lock dan https://developer.mozilla.org/en-US/docs/Web/API/Element/requestFullscreen . Dukungan fullscreen/penguncian orientasi bergantung browser. Tidak ada klaim pengujian perangkat fisik.

## Verifikasi

- Pengaturan Mode Guru default mati, tersimpan sesudah reload, dan tidak mengubah nilai/progres; diperiksa lewat unit check dan UI.
- Tampilan guru/anak dan pembaruan antar-tab diperiksa pada browser lokal.
- Dialog Mulai dan penghilangan footer diperiksa di ketiga game.
- Simulasi iframe 390×844 dan 844×390 memeriksa portrait/landscape; jalur native fullscreen serta fallback rotasi saat izin fullscreen ditolak diperiksa.
- Klik benda setelah rotasi tetap menemukan target dan memperbarui penghitung.
- Berkas uji viewport berada di output/mobile-layout-qa.html dan tidak masuk paket publik.
