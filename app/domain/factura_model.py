# app/domain/factura_model.py
from pydantic import BaseModel
from datetime import datetime
from typing import Literal

# Definición del tipo de estado para asegurar la consistencia
EstadoFactura = Literal["Pendiente", "Pagada", "Cancelada"]

class FacturaResponse(BaseModel):
    """
    Modelo para MOSTRAR las Facturas Pendientes (Resultado de HU-22: ConsultaF).
    """
    id: int
    id_paciente: int
    id_tratamiento: int
    monto_total: float
    monto_pendiente: float
    estado_factura: EstadoFactura
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True