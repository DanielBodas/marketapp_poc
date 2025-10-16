import os
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Prefer a single DATABASE_URL (e.g. postgres://...) coming from environment/secrets
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_URL")

# Si no hay URL de base de datos, hacer fallback a SQLite local para desarrollo/CI ligero.
# Si realmente quieres forzar el uso de una DB remota, exporta FORCE_ENV_DB=1 y entonces se lanzará error.
if not DATABASE_URL:
    if os.getenv("FORCE_ENV_DB"):
        raise ValueError("No se encontró DATABASE_URL o SUPABASE_URL en el archivo .env o en las variables de entorno")
    # fallback local
    import warnings
    warnings.warn("DATABASE_URL no encontrada; usando sqlite local 'sqlite:///./dev.db' para desarrollo.")
    DATABASE_URL = "sqlite:///./dev.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine():
    return engine

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_session():
    """Backward-compatible helper that returns a session instance.

    Prefer using `with session_scope() as session:` in new code.
    """
    return SessionLocal()