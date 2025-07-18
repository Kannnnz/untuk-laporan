# Struktur Aplikasi

Aplikasi ini telah direorganisasi dengan struktur folder yang lebih rapi dan terpisah antara backend dan frontend.

## Struktur Folder

```
app/
├── backend/           # Semua kode backend (FastAPI)
│   ├── api/          # Router dan endpoint API
│   ├── core/         # Konfigurasi aplikasi
│   ├── db/           # Database session dan koneksi
│   ├── exceptions/   # Custom exceptions
│   ├── main.py       # Entry point aplikasi FastAPI
│   ├── middleware/   # Middleware (CORS, dll)
│   ├── schemas/      # Pydantic models
│   ├── services/     # Business logic
│   └── utils/        # Utility functions
├── frontend/         # Semua file frontend
│   ├── index.html    # Halaman utama
│   ├── script.js     # JavaScript logic
│   └── styles.css    # Styling CSS
├── uploads/          # File upload storage
├── vector_store/     # Vector database files
└── README.md         # Dokumentasi ini
```

## Keuntungan Struktur Baru

1. **Pemisahan yang Jelas**: Backend dan frontend terpisah dengan jelas
2. **Mudah Dikembangkan**: Developer dapat fokus pada satu bagian tanpa terganggu yang lain
3. **Skalabilitas**: Struktur ini memudahkan pengembangan aplikasi yang lebih besar
4. **Dokumentasi**: Lebih mudah untuk mendokumentasikan dan memahami struktur aplikasi

## Cara Menjalankan

### Opsi 1: Menggunakan Script Startup (Direkomendasikan)
```bash
# Dari root directory project
python run_server.py
```

### Opsi 2: Menjalankan Manual
```bash
# Dari root directory project
cd app
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### Akses Aplikasi
- **Frontend**: http://127.0.0.1:8000/
- **API Documentation**: http://127.0.0.1:8000/docs
- **Alternative API Docs**: http://127.0.0.1:8000/redoc

## Perubahan Penting

- Semua import path telah diperbarui dari `app.*` menjadi `backend.*`
- Static files sekarang disajikan dari folder `frontend/`
- Struktur folder lebih modular dan mudah dipelihara