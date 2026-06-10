from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# ===== INIT =====
appjwt = FastAPI(title="FastAPI + Supabase + JWT (Toko Servis Laptop)")
security = HTTPBearer()

# ===== MIDDLEWARE CORS (Penghubung ke Front-End) =====
appjwt.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua browser/Front-End mengakses backend ini
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Mengizinkan semua header (termasuk token Authorization)
)

# ===== LOAD ENV =====
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE = os.getenv("TABLE")

BASE_URL = f"{SUPABASE_URL}/rest/v1/{TABLE}"

# ===== MODEL =====
class LoginRequest(BaseModel):
    email: str
    password: str

# Model Data Servis Laptop
class ServisLaptop(BaseModel):
    nama_pelanggan: str
    jenis_perangkat: str
    keluhan: str


# ===== HELPER =====
def safe_json(response):
    try:
        if response.text:
            return response.json()
        return {"message": "success"}
    except:
        return {"raw": response.text}


# ===== LOGIN (Mendapatkan Token dari Supabase) =====
@appjwt.post("/login")
def login(data: LoginRequest):
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"

    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json"
    }

    r = requests.post(url, headers=headers, json=data.dict())

    if r.status_code != 200:
        raise HTTPException(status_code=401, detail=r.text)

    return r.json()


# ===== VERIFY TOKEN (VALIDASI KE SUPABASE) =====
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    r = requests.get(
        f"{SUPABASE_URL}/auth/v1/user",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {token}"
        }
    )

    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Token tidak valid atau kedaluwarsa")

    return token


# ===== GET DATA (Harus Pakai Token) =====
@appjwt.get("/servis")
def get_data(token=Depends(verify_token)):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {token}"
    }

    r = requests.get(BASE_URL, headers=headers)

    return safe_json(r)


# ===== INSERT DATA (Harus Pakai Token) =====
@appjwt.post("/servis")
def create_data(data: ServisLaptop, token=Depends(verify_token)):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    r = requests.post(BASE_URL, headers=headers, json=data.dict())

    return safe_json(r)


# ===== UPDATE DATA (Harus Pakai Token) =====
@appjwt.put("/servis/{id}")
def update_data(id: str, data: ServisLaptop, token=Depends(verify_token)):
    url = f"{BASE_URL}?id=eq.{id}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    r = requests.patch(url, headers=headers, json=data.dict())

    return safe_json(r)


# ===== DELETE DATA (Harus Pakai Token) =====
@appjwt.delete("/servis/{id}")
def delete_data(id: str, token=Depends(verify_token)):
    url = f"{BASE_URL}?id=eq.{id}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {token}"
    }

    r = requests.delete(url, headers=headers)

    return safe_json(r)