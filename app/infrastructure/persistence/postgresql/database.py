# app/infrastructure/persistence/postgresql/database.py

import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

# ── 1. Leer y validar DATABASE_URL ────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL", "")

if not DATABASE_URL:
    raise RuntimeError(
        "La variable de entorno DATABASE_URL no está configurada. "
        "Agrégala en Azure Portal → Configuration → Environment variables."
    )

# ── 2. Fix para URLs con prefijo 'postgres://' (Heroku / Azure legacy) ────────
#    SQLAlchemy 2.x solo acepta 'postgresql://', no 'postgres://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    logger.info("DATABASE_URL corregida: prefijo cambiado a 'postgresql://'")

# ── 3. Crear engine con pool ajustado para Azure (conexiones limitadas en B1) ─
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # verifica conexión antes de usarla (evita "stale connections")
    pool_size=5,             # máximo de conexiones permanentes en el pool
    max_overflow=10,         # conexiones extra permitidas en pico de tráfico
    pool_recycle=1800,       # recicla conexiones cada 30 min (evita timeouts de la BD)
    echo=False,              # cambia a True temporalmente si quieres ver el SQL generado
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ── 4. Dependencia de FastAPI ─────────────────────────────────────────────────
def get_db():
    """Inyecta una sesión de BD por request y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── 5. Crear tablas + verificar conexión ──────────────────────────────────────
def create_tables():
    """Crea las tablas si no existen y verifica que la conexión sea válida."""
    # Import aquí para evitar imports circulares
    from app.infrastructure.persistence.postgresql.post_model import PostModel  # noqa: F401

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Conexión a PostgreSQL exitosa.")
    except Exception as e:
        logger.error(f"No se pudo conectar a PostgreSQL: {e}")
        raise

    Base.metadata.create_all(bind=engine)
    logger.info("✅ Tablas verificadas/creadas correctamente.")