document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");
    const currentPath = window.location.pathname;

    console.log("JS Ready. Path saat ini:", currentPath);
    console.log("Token yang tersimpan:", token);

    // Proteksi Halaman Berbasis Route
    if (!token && currentPath === "/dashboard") {
        window.location.replace("/");
        return;
    } else if (token && currentPath === "/") {
        window.location.replace("/dashboard");
        return;
    }

    // Aksi Form Login
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        console.log("Form login ditemukan!");
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            console.log("Tombol login diklik!");
            
            const email = document.getElementById("login-email").value;
            const password = document.getElementById("login-password").value;
            const alertBox = document.getElementById("login-alert");

            try {
                const response = await ApiClient.login(email, password);
                const result = await response.json();

                console.log("Respon dari server login:", result);

                if (response.ok) {
                    // Ambil token dari Supabase
                    const tokenToSave = result.access_token;
                    if (tokenToSave) {
                        localStorage.setItem("access_token", tokenToSave);
                        console.log("Token berhasil disimpan! Mengalihkan...");
                        // Paksa pindah ke halaman dashboard
                        window.location.href = "/dashboard";
                    } else {
                        alertBox.textContent = "Token tidak ditemukan dalam respon server.";
                        alertBox.classList.remove("d-none");
                    }
                } else {
                    alertBox.textContent = result.detail || "Gagal Login! Periksa email/password.";
                    alertBox.classList.remove("d-none");
                }
            } catch (error) {
                console.error("Error saat login:", error);
                alertBox.textContent = "Tidak dapat terhubung ke server backend.";
                alertBox.classList.remove("d-none");
            }
        });
    }

    // Aksi di Halaman Dashboard
    if (currentPath === "/dashboard") {
        loadData();

        const servisForm = document.getElementById("servis-form");
        if (servisForm) {
            servisForm.addEventListener("submit", async (e) => {
                e.preventDefault();
                const data = {
                    nama_pelanggan: document.getElementById("nama_pelanggan").value,
                    jenis_perangkat: document.getElementById("jenis_perangkat").value,
                    keluhan: document.getElementById("keluhan").value
                };

                const res = await ApiClient.addServis(data);
                if (res.ok) {
                    servisForm.reset();
                    loadData();
                } else {
                    alert("Gagal menambah data antrean.");
                }
            });
        }

        const logoutBtn = document.getElementById("logout-btn");
        if (logoutBtn) {
            logoutBtn.addEventListener("click", () => {
                localStorage.removeItem("access_token");
                window.location.replace("/");
            });
        }
    }
});

async function loadData() {
    const tbody = document.getElementById("tabel-servis-body");
    if (!tbody) return;
    
    try {
        const res = await ApiClient.fetchServis();
        if (res.status === 401) {
            localStorage.removeItem("access_token");
            window.location.replace("/");
            return;
        }
        const data = await res.json();
        tbody.innerHTML = "";
        
        if (Array.isArray(data)) {
            data.forEach(item => {
                tbody.innerHTML += `<tr><td>${item.nama_pelanggan}</td><td>${item.jenis_perangkat}</td><td>${item.keluhan}</td></tr>`;
            });
        }
    } catch (err) {
        console.error("Gagal memuat data tabel:", err);
    }
}