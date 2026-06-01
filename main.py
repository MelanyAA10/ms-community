# main.py
import os
import logging
from fastapi import FastAPI
from app.infrastructure.persistence.postgresql.database import create_tables
from app.infrastructure.web.routers.posts_router import router as posts_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="BookLoop Community API")


@app.on_event("startup")
def startup():
    # No tumbamos la app si la BD falla al arrancar: registramos el error para
    # poder verlo en el Log stream, pero dejamos que / y /health respondan para
    # poder diagnosticar (p. ej. saber si DATABASE_URL esta puesta).
    try:
        create_tables()
    except Exception as e:
        logger.error(f"create_tables() fallo al arrancar: {e}")


app.include_router(posts_router)


@app.get("/")
def root():
    return {"message": "ms-community is running"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "database_url_set": bool(os.getenv("DATABASE_URL")),
    }