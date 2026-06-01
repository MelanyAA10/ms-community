# main.py
from fastapi import FastAPI
import os
from app.infrastructure.persistence.postgresql.database import create_tables
from app.infrastructure.web.routers.posts_router import router as posts_router

app = FastAPI(title="BookLoop Community API")

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(posts_router)

@app.get("/")
def root():
    return {"message": "ms-community is running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "database_url_set": bool(os.getenv("DATABASE_URL"))
    }