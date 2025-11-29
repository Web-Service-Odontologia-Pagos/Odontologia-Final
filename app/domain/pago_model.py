# app/domain/pago_model.py
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

EstadoPago = Literal["En Proceso", "Pagado", "Rechazado"]

# ============================================================================
# MODELOS PARA HU-21: INICIO DE PAGO (IPago)
# ============================================================================

class PagoRequest(BaseModel):
    """
    Modelo para RECIBIR datos sensibles del cliente (HU-21: IPago).
    """
    id_factura: int = Field(..., description="ID de la factura seleccionada por el cliente.")
    monto_pagado: float = Field(..., gt=0, description="Monto que el cliente desea pagar.")

    # Campos sensibles requeridos por HU-21
    datos_tarjeta: str = Field(..., min_length=12, max_length=19, description="Número de tarjeta de crédito/débito.")
    pin_seguridad: str = Field(..., min_length=3, max_length=4, description="PIN/CVV de la tarjeta.")


# ============================================================================
# MODELOS PARA HU-24 y HU-26: VALIDACIÓN Y CAMBIO DE ESTADO (ValidaciónP)
# ============================================================================

class ValidacionPRequest(BaseModel):
    """
    Modelo para RECIBIR validación/notificación del banco (HU-24: ValidaciónP).
    Equivalente JSON del XML/SOAP que proporcionaste.
    
    Estructura original XML:
    <pag:ValidaciónP>
        <pag:Estado>Pagado</pag:Estado>
        <pag:idTransaccion>ABC123XYZ</pag:idTransaccion>
    </pag:ValidaciónP>
    """
    estado: EstadoPago = Field(..., description="Estado final de la transacción (Pagado/Rechazado/En Proceso)")
    id_transaccion: str = Field(..., min_length=5, max_length=50, description="ID único de la transacción del banco (ej: ABC123XYZ)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "estado": "Pagado",
                "id_transaccion": "ABC123XYZ"
            }
        }


class CambioEPRequest(BaseModel):
    """
    Modelo para ACTUALIZAR el estado de pago (HU-26: CambioEP).
    """
    id_pago: int = Field(..., description="ID del registro de pago a modificar.")
    estado_final: EstadoPago = Field(..., description="Estado final de la transacción ('Pagado' o 'Rechazado').")
    id_transaccion_banco: str = Field(..., description="ID de referencia único proporcionado por el banco.")


# ============================================================================
# MODELOS PARA RESPUESTAS
# ============================================================================

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


class ValidacionPResponse(BaseModel):
    """
    Respuesta del servidor al recibir validación del banco (HU-24).
    """
    mensaje: str = Field(..., description="Mensaje de confirmación")
    id_transaccion: str = Field(..., description="ID de transacción confirmado")
    estado_actualizado: EstadoPago = Field(..., description="Estado actual del pago")
    
    class Config:
        json_schema_extra = {
            "example": {
                "mensaje": "Estado recibido y actualización interna (CambioEP) disparada con éxito.",
                "id_transaccion": "ABC123XYZ",
                "estado_actualizado": "Pagado"
            }
        }