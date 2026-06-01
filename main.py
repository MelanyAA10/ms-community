from fastapi import FastAPI
import os

app = FastAPI(title="BookLoop Community API")

@app.get("/")
def root():
    return {"message": "ms-community is running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "database_url_set": bool(os.getenv("DATABASE_URL"))
    }