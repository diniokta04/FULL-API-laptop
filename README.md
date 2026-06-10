# FULL-API-laptop
Berikut adalah penjelasan ringkas mengenai 3 komponen utama dalam sistem yang baru saja kamu buat:

1. RESTful API (Backend)
Jembatan penghubung antara aplikasi depan (Front-End) dan database. Menggunakan FastAPI, backend ini bertugas menerima permintaan (request) dari pengguna, memeriksa keamanannya, lalu mengeksekusi perintah seperti mengambil data (GET) atau menambah data (POST).

2. JWT (JSON Web Token)
Karcis digital sebagai bukti bahwa kamu sudah login. Saat kamu berhasil memasukkan email dan password yang benar di menu /login, server akan memberikan token berupa teks acak yang panjang. Token inilah yang wajib dibawa di setiap transaksi data agar sistem tahu kamu adalah pengguna yang sah.

3. CORS (Cross-Origin Resource Sharing)
Aturan keamanan pada browser. Secara standar, browser akan memblokir jika ada file HTML lokal (index.html) mencoba menembak data ke server lain (FastAPI di port 8000). Kode middleware CORS yang kita masukkan berfungsi memberikan izin resmi agar browser tidak memblokir komunikasi tersebut.
