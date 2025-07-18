# setup.py (FINAL VERSION for the new structured project)

import mysql.connector
import bcrypt
from datetime import datetime
from pathlib import Path
import sys

# --- SETUP PATH & IMPORT CONFIG ---
# Trik untuk menambahkan direktori 'app' ke path Python
# agar kita bisa mengimpor modul konfigurasi dari sana.
# Ini membuat skrip setup konsisten dengan aplikasi utama.
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    # Impor konfigurasi dari file pusat kita di app/core/config.py
    from app.core import config
except ImportError:
    print("❌ Gagal mengimpor konfigurasi dari 'app.core.config'.")
    print("Pastikan Anda menjalankan setup.py dari direktori root proyek dan struktur folder sudah benar.")
    sys.exit(1)


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.
    Fungsi ini harus konsisten dengan yang ada di aplikasi utama.
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def setup_environment():
    """Membuat direktori yang diperlukan berdasarkan path dari config."""
    print("🚀 Memeriksa direktori yang diperlukan...")
    # Menggunakan path dari config.py sebagai satu-satunya sumber kebenaran
    config.UPLOAD_DIR.mkdir(exist_ok=True)
    config.VECTOR_STORE_DIR.mkdir(exist_ok=True)
    print(f"✅ Direktori Uploads di '{config.UPLOAD_DIR}' siap.")
    print(f"✅ Direktori Vector Store di '{config.VECTOR_STORE_DIR}' siap.")

def setup_database():
    """
    Menginisialisasi database MySQL dengan tabel yang diperlukan
    dan membuat akun admin default.
    """
    try:
        # 1. Koneksi ke server MySQL untuk membuat database jika belum ada
        print(f"🚀 Mencoba terhubung ke server MySQL di '{config.DB_HOST}'...")
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        cursor = conn.cursor()
        print(f"✅ Berhasil terhubung ke server MySQL.")
        print(f"✨ Membuat database '{config.DB_NAME}' jika belum ada...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.close()
        conn.close()
        print(f"✅ Database '{config.DB_NAME}' siap digunakan.")

        # 2. Koneksi ke database spesifik untuk membuat tabel
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )
        cursor = conn.cursor()
        
        # 3. Hapus tabel lama untuk setup yang bersih (opsional tapi disarankan untuk awal)
        print("⚠️  Menghapus tabel lama (jika ada) untuk setup yang bersih...")
        cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
        cursor.execute('DROP TABLE IF EXISTS chat_history')
        cursor.execute('DROP TABLE IF EXISTS documents')
        cursor.execute('DROP TABLE IF EXISTS users')
        cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
        print("✅ Tabel lama berhasil dihapus.")

        # 4. Membuat struktur tabel baru (Sama seperti sebelumnya)
        print("🏗️  Membuat struktur tabel baru...")
        cursor.execute('''
        CREATE TABLE users (
            username VARCHAR(255) PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(256) NOT NULL, role VARCHAR(50) NOT NULL DEFAULT 'user',
            created_at DATETIME NOT NULL
        ) ENGINE=InnoDB
        ''')
        cursor.execute('''
        CREATE TABLE documents (
            id VARCHAR(36) PRIMARY KEY, username VARCHAR(255) NOT NULL, filename TEXT NOT NULL,
            file_path TEXT NOT NULL, upload_date DATETIME NOT NULL, file_size BIGINT,
            is_indexed BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
        ) ENGINE=InnoDB
        ''')
        cursor.execute('''
        CREATE TABLE chat_history (
            id INT PRIMARY KEY AUTO_INCREMENT, session_id VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL, message TEXT NOT NULL, response TEXT NOT NULL,
            timestamp DATETIME NOT NULL, document_ids JSON,
            FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE,
            INDEX idx_chat_history_session_id (session_id)
        ) ENGINE=InnoDB
        ''')
        conn.commit()
        print("✅ Semua tabel berhasil dibuat.")

        # 5. Buat admin default dari variabel .env
        print("\n🔑 Mengecek akun admin...")
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        if cursor.fetchone()[0] == 0:
            print("📋 Tidak ada admin. Membuat admin default...")
            # Menggunakan password dari config yang dimuat dari .env
            admin_pass = hash_password(config.DEFAULT_ADMIN_PASSWORD) 
            cursor.execute(
                "INSERT INTO users (username, email, password, role, created_at) VALUES (%s, %s, %s, %s, %s)",
                ('admin', 'admin@mail.unnes.ac.id', admin_pass, 'admin', datetime.now())
            )
            conn.commit()
            print(f"✅ Admin default 'admin' berhasil dibuat. Gunakan password dari file .env Anda untuk login.")
        else:
            print("✅ Akun admin sudah ada.")

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as err:
        print(f"\n❌ GAGAL melakukan setup database MySQL: {err}")
        print("   Pastikan kredensial database di file .env Anda sudah benar dan server MySQL sedang berjalan.")
        return False

if __name__ == "__main__":
    print("==========================================")
    print("🚀 UNNES Document Chat System - Setup 🚀")
    print("==========================================")
    
    # Memberikan peringatan jika password default tidak diubah
    if not config.DEFAULT_ADMIN_PASSWORD or config.DEFAULT_ADMIN_PASSWORD == "adminUnnesKuat123!":
        print("🔥 PERINGATAN: Anda masih menggunakan password admin default di file .env.")
        print("   Sangat disarankan untuk mengubah `DEFAULT_ADMIN_PASSWORD` demi keamanan.\n")
        
    setup_environment()
    if setup_database():
        print("\n🎉 Setup selesai dengan sukses!")
        print("📌 Selanjutnya, jalankan server dengan perintah:")
        print("   uvicorn app.main:app --reload")
