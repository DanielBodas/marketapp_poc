import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Cargar la contraseña desde el .env
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")

if not SUPABASE_PASSWORD:
    raise ValueError("No se encontró SUPABASE_PASSWORD en el archivo .env")

# Cadena de conexión con la contraseña interpolada
SUPABASE_URL = f"postgresql://postgres.yanxbtceflobfgxwvtaz:{SUPABASE_PASSWORD}@aws-1-eu-west-1.pooler.supabase.com:6543/postgres"

engine = create_engine(SUPABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine():
    return engine

def get_session():
    return SessionLocal()