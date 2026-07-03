# 🛠️ Sistem Manajemen Antrean Toko Servis Laptop

Sistem manajemen antrean dan pendataan servis laptop berbasis web yang dibangun menggunakan **FastAPI** sebagai backend, **Supabase Auth & Database** sebagai media penyimpanan data serta autentikasi, dan **JSON Web Token (JWT)** sebagai sistem keamanannya. 

Project ini dirancang menggunakan **Arsitektur Modular Full-Stack Local**, di mana file logika backend, aset statis (CSS/JS), dan tampilan halaman (HTML Templates) dipisahkan secara terstruktur demi kemudahan pengembangan dan pengelolaan kode.

---

## 📁 Struktur Folder Project

Aplikasi ini menerapkan struktur folder yang rapi dan terintegrasi penuh di dalam server lokal backend:

```text
servic_laptop/
│
├── app.py                       # File utama Backend FastAPI & Konfigurasi Rute
├── .env                         # File konfigurasi raia (Supabase URL & API Key)
├── .gitignore                   # Pengabaian file rahasia agar tidak masuk GitHub
│
└── python_app/                  # Folder utama aplikasi web terintegrasi
    ├── static/                  # Menyimpan seluruh aset statis aplikasi
    │   ├── css/
    │   │   └── styles.css       # Desain tampilan kustom halaman web
    │   └── js/
    │       ├── api-client.js    # Modul khusus penanganan fetch data ke API Backend
    │       └── app.js           # Logika interaksi DOM, form, dan proteksi halaman
    │
    └── templates/               # Menyimpan file halaman web (HTML)
        ├── login.html           # Tampilan halaman masuk sistem
        └── dashboard.html       # Tampilan antrean servis & form input data
