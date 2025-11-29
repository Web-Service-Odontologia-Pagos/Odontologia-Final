# app/domain/factura_model.py
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Literal, List, Optional

# Definición del tipo de estado para asegurar la consistencia
EstadoFactura = Literal["Pendiente", "Pagada", "Cancelada"]

# ============================================================================
# MODELOS BÁSICOS
# ============================================================================

class FacturaResponse(BaseModel):
    """
    Modelo para MOSTRAR una Factura Individual.
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


# ============================================================================
# MODELO PARA DETALLE DE FACTURA EN CONSULTA (HU-22)
# ============================================================================

class DetalleFactura(BaseModel):
    """
    Detalle de cada factura en la respuesta de ConsultaF (HU-22).
    Basado en la estructura proporcionada.
    """
    id_factura: int = Field(..., description="ID único de la factura")
    monto: float = Field(..., gt=0, description="Monto total de la factura")
    monto_pendiente: Optional[float] = Field(None, description="Monto aún pendiente de pago")
    estado: EstadoFactura = Field(..., description="Estado actual de la factura")
    fecha_creacion: Optional[datetime] = Field(None, description="Fecha de creación")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id_factura": 101,
                "monto": 4500000,
                "monto_pendiente": 4500000,
                "estado": "Pendiente",
                "fecha_creacion": "2025-07-31T00:00:00"
            }
        }


# ============================================================================
# MODELO PARA RESPUESTA DE CONSULTA DE SALDOS (HU-22: ConsultaF)
# ============================================================================

class ConsultaSaldosData(BaseModel):
    """
    Datos detallados de la consulta de saldos.
    Estructura inspirada en la proporcionada.
    """
    fecha_proceso: date = Field(..., description="Fecha en que se realiza la consulta")
    capital_total: float = Field(..., description="Suma de montos totales de todas las facturas pendientes")
    intereses_causados: float = Field(default=0, description="Intereses generados por mora (opcional)")
    intereses_contingentes: float = Field(default=0, description="Intereses contingentes (opcional)")
    detalle_facturas: List[DetalleFactura] = Field(..., description="Lista de facturas pendientes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "fecha_proceso": "2025-07-31",
                "capital_total": 8500000,
                "intereses_causados": 2400000,
                "intereses_contingentes": 1200000,
                "detalle_facturas": [
                    {
                        "id_factura": 101,
                        "monto": 4500000,
                        "monto_pendiente": 4500000,
                        "estado": "Pendiente",
                        "fecha_creacion": "2025-07-31T00:00:00"
                    }
                ]
            }
        }


class ConsultaFacturasResponse(BaseModel):
    """
    Respuesta completa para HU-22: ConsultaF (Consulta de Facturas Pendientes).
    
    Estructura general:
    - mensaje: Mensaje descriptivo de la operación
    - data: Datos detallados de la consulta
    - success: Indicador de éxito de la operación
    """
    mensaje: str = Field(..., description="Mensaje descriptivo del resultado")
    data: ConsultaSaldosData = Field(..., description="Datos detallados de saldos y facturas")
    success: bool = Field(default=True, description="Indica si la consulta fue exitosa")
    
    class Config:
        json_schema_extra = {
            "example": {
                "mensaje": "Consulta de saldos exitosa",
                "data": {
                    "fecha_proceso": "2025-07-31",
                    "capital_total": 8500000,
                    "intereses_causados": 2400000,
                    "intereses_contingentes": 1200000,
                    "detalle_facturas": [
                        {
                            "id_factura": 101,
                            "monto": 4500000,
                            "monto_pendiente": 4500000,
                            "estado": "Pendiente",
                            "fecha_creacion": "2025-07-31T00:00:00"
                        }
                    ]
                },
                "success": True
            }
        }


# ============================================================================
# MODELO PARA CREAR/ACTUALIZAR FACTURA (INTERNO)
# ============================================================================

class FacturaCreate(BaseModel):
    """
    Modelo para CREAR una nueva factura (uso interno).
    """
    id_paciente: int = Field(..., gt=0, description="ID del paciente propietario")
    id_tratamiento: int = Field(..., gt=0, description="ID del tratamiento realizado")
    monto_total: float = Field(..., gt=0, description="Monto total a facturar")
    monto_pendiente: Optional[float] = Field(None, description="Monto pendiente (default: igual al total)")
    estado_factura: EstadoFactura = Field(default="Pendiente", description="Estado inicial")