from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from backend.core import config
from backend.api.routers import auth, documents, chat, admin
from backend.middleware.cors_middleware import add_cors_middleware

config.UPLOAD_DIR.mkdir(exist_ok=True)
config.VECTOR_STORE_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="UNNES Document Chat System (Structured Version)",
    version="7.0.0"
)

# Add middleware
add_cors_middleware(app)

API_V1_PREFIX = "/api/v1"
app.include_router(auth.router, prefix=f"{API_V1_PREFIX}/auth")
app.include_router(documents.router, prefix=f"{API_V1_PREFIX}/documents")
app.include_router(chat.router, prefix=f"{API_V1_PREFIX}/chat")
app.include_router(admin.router, prefix=f"{API_V1_PREFIX}/admin")

STATIC_DIR = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=FileResponse, include_in_schema=False)
async def read_index():
    return FileResponse(STATIC_DIR / 'index.html')

@app.get("/health", tags=["System"])
def health_check():
    from backend.db.session import db_pool
    from backend.services.rag_service import rag_service
    
    db_status = "connected" if db_pool and db_pool.get_connection().is_connected() else "disconnected"
    rag_status = "connected" if rag_service.is_ready else "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" and rag_status == "connected" else "degraded",
        "database": db_status,
        "llm_ollama": rag_status
    }