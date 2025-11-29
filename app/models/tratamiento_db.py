from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class TratamientoDB(Base):
    """
    Tabla de Tratamientos. Necesaria para HU-22 para consolidar el monto.
    """
    __tablename__ = "tratamientos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    costo_total = Column(Float, nullable=False)