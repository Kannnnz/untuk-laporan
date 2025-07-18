#!/usr/bin/env python3
"""
Startup script untuk menjalankan aplikasi dengan struktur folder yang baru.
Script ini akan menjalankan server FastAPI dari folder backend.
"""

import sys
import os
from pathlib import Path

# Tambahkan path app ke sys.path agar import backend bisa bekerja
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

if __name__ == "__main__":
    import uvicorn
    
    # Jalankan server dari backend.main
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[str(app_dir / "backend"), str(app_dir / "frontend")]
    )