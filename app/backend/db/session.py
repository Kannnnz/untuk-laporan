import mysql.connector.pooling
from contextlib import contextmanager
from backend.core import config
from backend.exceptions.custom_exceptions import DatabaseError

db_pool = None
try:
    db_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="unnes_pool",
        pool_size=10,
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )
    print("✅ Database connection pool berhasil dibuat.")
except mysql.connector.Error as err:
    print(f"❌ Gagal membuat database connection pool: {err}")

@contextmanager
def get_db_connection():
    if not db_pool:
        raise DatabaseError("Database service not available.")
    connection = None
    try:
        connection = db_pool.get_connection()
        yield connection
    except mysql.connector.Error as err:
        raise DatabaseError(f"Database connection error: {err}")
    finally:
        if connection and connection.is_connected():
            connection.close()