import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
FAISS_INDEX_PATH = VECTOR_STORE_DIR / "unnes_docs.faiss"

SECRET_KEY = os.getenv("APP_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD", "adminUnnesKuat123!")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

if not SECRET_KEY or SECRET_KEY == "ganti_dengan_kunci_rahasia_yang_sangat_aman_dan_panjang":
    raise ValueError("APP_SECRET_KEY tidak diatur di file .env. Ini sangat tidak aman.")

if not GOOGLE_CLIENT_ID:
    print("⚠️  PERINGATAN: GOOGLE_CLIENT_ID tidak diatur di file .env. Fitur Login dengan Google tidak akan berfungsi.")
