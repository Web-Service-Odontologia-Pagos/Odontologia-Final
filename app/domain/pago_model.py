# app/domain/pago_model.py
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

EstadoPago = Literal["En Proceso", "Pagado", "Rechazado"]

class PagoRequest(BaseModel):
    """
    Modelo para RECIBIR datos sensibles del cliente (HU-21: IPago).
    """
    id_factura: int = Field(..., description="ID de la factura seleccionada por el cliente.")
    monto_pagado: float = Field(..., gt=0, description="Monto que el cliente desea pagar.")

    # Campos sensibles requeridos por HU-21
    datos_tarjeta: str = Field(..., min_length=12, max_length=19, description="Número de tarjeta de crédito/débito.")
    pin_seguridad: str = Field(..., min_length=3, max_length=4, description="PIN/CVV de la tarjeta.")


class CambioEPRequest(BaseModel):
    """
    Modelo para ACTUALIZAR el estado de pago (HU-26: CambioEP).
    """
    id_pago: int = Field(..., description="ID del registro de pago a modificar.")
    estado_final: EstadoPago = Field(..., description="Estado final de la transacción ('Pagado' o 'Rechazado').")
    id_transaccion_banco: str = Field(..., description="ID de referencia único proporcionado por el banco.")


class PagoResponse(BaseModel):
    """
    Modelo para MOSTRAR el estado de un registro de pago.
    """
    id: int
    id_factura: int
    estado_pago: EstadoPago
    fecha_inicio: datetime
    id_transaccion_banco: Optional[str] = None
    
    class Config:
        from_attributes = True