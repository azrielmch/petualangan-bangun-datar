# WebP kualitas 85

- Seluruh 75 PNG dalam assets-3d dan tiga latar sumber dikonversi ke WebP kualitas 85.
- PNG di dalam SVG juga dikonversi; geometri/markup vektor tetap.
- Dimensi dan nilai alpha diperiksa identik; warna/tekstur dikompresi secara lossy sesuai pilihan pemilik.
- Nama aset berubah dari .png ke .webp; rujukan halaman, CSS, JavaScript, konfigurasi dan sumber pembangun sudah disesuaikan.
- File asli disimpan di ../../arsip-lokal/sebelum-webp85/, di luar repositori.
- Ukuran assets-3d: 310.610.001 byte menjadi 29.942.515 byte (hemat 90,36%). Ini ukuran total folder, bukan pengukuran waktu loading. Game hanya mengambil aset sesi yang dipilih; hasil pada jaringan HP dapat berbeda.
- Versi cache webp85-9 memastikan browser mengambil konfigurasi dan kode baru.
- Publikasi dilakukan melalui repositori GitHub yang terhubung ke Vercel.

Pemeriksaan: 81 gambar unik telah didekode dan diverifikasi dimensi/alpha, semua 806 SVG valid, serta pemeriksaan 6.000 sesi acak lulus.
