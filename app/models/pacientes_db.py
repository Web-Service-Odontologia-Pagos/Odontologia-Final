from sqlalchemy import Column, Integer, String
from app.database import Base


class PacienteDB(Base):
    """
    Tabla de Pacientes. Necesaria para HU-22 (Consulta) y HU-23 (Notificación).
    """
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)