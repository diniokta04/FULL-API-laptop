from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# ===== INIT APP =====
appjwt = FastAPI(title="FastAPI + Supabase + JWT (Toko Servis Laptop)")

# ===== CONFIG TEMPLATES & STATIC =====
# Menghubungkan folder static dan templates sesuai struktur baru
appjwt.mount("/static", StaticFiles(directory="python_app/static"), name="static")
templates = Jinja2Templates(directory="python_app/templates")

security = HTTPBearer()

# ===== MIDDLEWARE CORS =====
appjwt.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

class ServisLaptop(BaseModel):
    nama_pelanggan: str
    jenis_perangkat: str
    keluhan: str

# ===== VERIFY TOKEN =====
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    r = requests.get(
        f"{SUPABASE_URL}/auth/v1/user",
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {token}"}
    )
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Token tidak valid atau kedaluwarsa")
    return token

# ================= ROUTE TAMPILAN (WEB PAGES) =================

@appjwt.get("/", response_class=HTMLResponse)
def rute_login(request: Request):
    # Merender halaman login.html dari folder templates
    return templates.TemplateResponse("login.html", {"request": request})

@appjwt.get("/dashboard", response_class=HTMLResponse)
def rute_dashboard(request: Request):
    # Merender halaman dashboard.html dari folder templates
    return templates.TemplateResponse("dashboard.html", {"request": request})

# ================= ROUTE API DATA (ENDPOINT) =================

@appjwt.post("/api/login")
def login(data: LoginRequest):
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    headers = {"apikey": SUPABASE_KEY, "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=data.dict())
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Login Gagal")
    return r.json()

@appjwt.get("/api/servis")
def get_data(token=Depends(verify_token)):
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {token}"}
    r = requests.get(BASE_URL, headers=headers)
    return r.json()

@appjwt.post("/api/servis")
def create_data(data: ServisLaptop, token=Depends(verify_token)):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    r = requests.post(BASE_URL, headers=headers, json=data.dict())
    return r.json()