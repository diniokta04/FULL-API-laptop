const API_BASE_URL = "http://127.0.0.1:8000";

const ApiClient = {
    async login(email, password) {
        const response = await fetch(`${API_BASE_URL}/api/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        return response;
    },
    async fetchServis() {
        const token = localStorage.getItem("access_token");
        return fetch(`${API_BASE_URL}/api/servis`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` } // Diperbaiki: Menggunakan backtick dan $ standar
        });
    },
    async addServis(data) {
        const token = localStorage.getItem("access_token");
        return fetch(`${API_BASE_URL}/api/servis`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` // Diperbaiki: Menggunakan backtick dan $ standar
            },
            body: JSON.stringify(data)
        });
    }
};