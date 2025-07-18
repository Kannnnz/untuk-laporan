from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

def add_cors_middleware(app: FastAPI):
    """Add CORS middleware to the FastAPI application"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )