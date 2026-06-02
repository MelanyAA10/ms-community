# app/infrastructure/persistence/postgresql/database.py

import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

# -- 1. Leer DATABASE_URL (sin reventar al importar) ---------------------------
#    IMPORTANTE: este modulo NO debe lanzar excepciones a nivel de import. Si lo
#    hace, FastAPI nunca define "app" y Azure no puede arrancar uvicorn, dando un
#    404 / "Issues Detected" sin pista clara. En su lugar dejamos el engine en
#    None y reportamos el estado por /health; create_tables() falla de forma
#    controlada y registrada en el Log stream.
def _normalize_url(url: str) -> str:
    # SQLAlchemy 2.x solo acepta 'postgresql://', no el viejo 'postgres://'.
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
        logger.info("DATABASE_URL: prefijo 'postgres://' corregido a 'postgresql://'.")
    return url


DATABASE_URL = _normalize_url(os.getenv("DATABASE_URL", "").strip())

# -- 2. Crear engine de forma perezosa -----------------------------------------
engine = None
SessionLocal = None
Base = declarative_base()


def _build_engine():
    """Crea el engine y el sessionmaker la primera vez que se necesitan."""
    global engine, SessionLocal
    if engine is not None:
        return
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL no esta configurada. Agregala en Azure Portal -> "
            "Settings -> Environment variables (o Configuration)."
        )
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,   # evita usar conexiones muertas (Azure corta las inactivas)
        pool_size=5,
        max_overflow=10,
        pool_recycle=1800,    # recicla cada 30 min
        echo=False,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# -- 3. Dependencia de FastAPI -------------------------------------------------
def get_db():
    """Inyecta una sesion de BD por request y la cierra al terminar."""
    _build_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -- 4. Crear tablas + verificar conexion --------------------------------------
def create_tables():
    """Crea las tablas si no existen y verifica que la conexion sea valida."""
    # Import aqui para registrar los modelos en Base y evitar imports circulares
    from app.infrastructure.persistence.postgresql.post_model import PostModel  # noqa: F401
    from app.infrastructure.persistence.postgresql.comment_model import CommentModel  # noqa: F401

    _build_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("Conexion a PostgreSQL exitosa.")

    Base.metadata.create_all(bind=engine)
    logger.info("Tablas verificadas/creadas correctamente.")