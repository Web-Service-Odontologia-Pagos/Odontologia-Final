# app/domain/tratamiento_model.py
from pydantic import BaseModel

class TratamientoResponse(BaseModel):
    """Modelo para MOSTRAR los detalles del tratamiento consolidado en una factura."""
    id: int
    nombre: str
    costo_total: float

    class Config:
        from_attributes = True