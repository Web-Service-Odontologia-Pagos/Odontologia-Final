# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- CONFIGURACIÓN DE LA CONEXIÓN ---
DATABASE_URL = "sqlite:///./odontologia_db.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# --- FUNCIONES DE UTILIDAD ---

def get_db():
    """
    Función de dependencia que maneja el ciclo de vida de la sesión de base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crea todas las tablas definidas anteriormente al inicio de la aplicación.
    """
    Base.metadata.create_all(bind=engine)