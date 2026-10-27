# Perbaikan HP — lokal

- Tombol layar penuh hanya di beranda. Shell tetap berada di halaman yang sama; navigasi permainan, hasil, pengaturan dan petunjuk berlangsung di iframe satu origin. Fullscreen native tidak hilang saat pindah game.
- Jika native fullscreen ditolak/tidak tersedia, seluruh viewport aplikasi diputar landscape, termasuk dialog dan halaman hasil, bukan main saja.
- iPhone: manifest standalone dan meta Apple. Pengguna diberi petunjuk Safari > Bagikan > Tambahkan ke Layar Utama. Browser biasa tidak dijanjikan bisa menyembunyikan bilah navigasi.
- AudioContext dipakai bersama dalam setiap halaman dan diaktifkan melalui pointer/keyboard. Efek klik, benar, salah, dan selesai mengikuti preferensi suara.
- Mode Guru meminta kode 1324, kode salah ditolak. Otorisasi sesi tidak diwariskan dari preferensi versi lama. Ini pengunci antarmuka lokal, bukan autentikasi server.
- Diuji di browser desktop: kode salah/benar, fullscreen dengan perpindahan ke game, simulasi 390x844 dengan fullscreen native ditolak dan popup selesai level mengikuti landscape. Belum diverifikasi di iPhone fisik.
- Diterbitkan sebagai versi publik 3 pada 27 Oktober 2026.
