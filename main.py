from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.persistence.postgresql.database import create_tables
from app.infrastructure.web.routers import posts_router

app = FastAPI(
    title="BookLoop Community API",
    description="Microservicio de comunidad para BookLoop",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    create_tables()

app.include_router(posts_router.router, prefix="/v1/community", tags=["Community"])

@app.get("/health")
def health():
    return {"status": "ok"}
