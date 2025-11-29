# app/api/factura_api.py

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import date, datetime
from typing import List

# Modelos (Domain Layer)
from app.domain.factura_model import (
    FacturaResponse, 
    ConsultaFacturasResponse,
    DetalleFactura,
    ConsultaSaldosData,
    FacturaCreate
)

# Servicios (Business Logic Layer)
from app.services.factura_service import FacturaService

# Router para la gestión de facturas
# Ruta definida en HU-22: /usuarios/{id}/consultaF
router = APIRouter(prefix="/usuarios", tags=["Facturas (HU-22)"])


# ============================================================================
# HU-22: CONSULTA DE FACTURAS PENDIENTES (ConsultaF)
# ============================================================================

@router.get(
    "/{paciente_id}/consultaF",
    response_model=ConsultaFacturasResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar Facturas Pendientes",
    description="Retorna todas las facturas pendientes de un paciente con saldos consolidados."
)
def get_facturas_pendientes_endpoint(
    paciente_id: int = Path(..., gt=0, description="ID del paciente a consultar"),
    db: Session = Depends(get_db)
):
    """
    **[HU-22: ConsultaF]** - Consulta de Facturas Pendientes
    
    Retorna la lista consolidada de facturas en estado 'Pendiente' para un paciente específico.
    
    **Incluye:**
    - Fecha de proceso (hoy)
    - Capital total adeudado (suma de montos pendientes)
    - Intereses causados (opcional, para futuras integraciones)
    - Intereses contingentes (opcional, para futuras integraciones)
    - Detalle de cada factura con:
      - ID de factura
      - Monto total
      - Monto pendiente
      - Estado actual
      - Fecha de creación
    
    **Respuesta exitosa (200 OK):**
    ```json
    {
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
        "success": true
    }
    ```
    
    **Casos especiales:**
    - Si no hay facturas pendientes: Retorna `capital_total: 0` y lista vacía
    - Estados posibles: "Pendiente", "Pagada", "Cancelada"
    """
    service = FacturaService(db)
    return service.consultar_saldos_paciente(paciente_id)


# ============================================================================
# ENDPOINTS ADICIONALES PARA GESTIÓN DE FACTURAS (INTERNOS)
# ============================================================================

@router.get(
    "/{paciente_id}/facturas",
    response_model=List[FacturaResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar Todas las Facturas",
    description="Retorna todas las facturas (pendientes, pagadas, canceladas) de un paciente."
)
def get_todas_facturas_endpoint(
    paciente_id: int = Path(..., gt=0, description="ID del paciente"),
    db: Session = Depends(get_db)
):
    """
    **Endpoint Adicional** - Listar todas las facturas de un paciente.
    
    A diferencia de ConsultaF (HU-22) que solo retorna pendientes,
    este endpoint retorna TODAS las facturas con cualquier estado.
    
    **Respuesta (200 OK):**
    ```json
    [
        {
            "id": 1,
            "id_paciente": 5,
            "id_tratamiento": 10,
            "monto_total": 500000,
            "monto_pendiente": 0,
            "estado_factura": "Pagada",
            "fecha_creacion": "2025-07-31T00:00:00"
        }
    ]
    ```
    """
    service = FacturaService(db)
    return service.get_facturas_pendientes_by_paciente(paciente_id)


@router.post(
    "/{paciente_id}/facturas",
    response_model=FacturaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear Nueva Factura",
    description="Crea una nueva factura para un paciente (uso interno)."
)
def create_factura_endpoint(
    paciente_id: int = Path(..., gt=0, description="ID del paciente"),
    factura_data: FacturaCreate = None,
    db: Session = Depends(get_db)
):
    """
    **Endpoint Adicional** - Crear nueva factura.
    
    Uso interno: se crea automáticamente cuando se realiza un tratamiento.
    
    **Request body (JSON):**
    ```json
    {
        "id_paciente": 5,
        "id_tratamiento": 10,
        "monto_total": 500000,
        "monto_pendiente": 500000,
        "estado_factura": "Pendiente"
    }
    ```
    
    **Campos requeridos:**
    - `id_tratamiento`: ID del tratamiento realizado
    - `monto_total`: Monto a facturar (debe ser > 0)
    
    **Campos opcionales:**
    - `monto_pendiente`: Si no se proporciona, se iguala al monto_total
    - `estado_factura`: Default "Pendiente"
    """
    if factura_data is None:
        raise HTTPException(status_code=400, detail="Datos de factura requeridos")
    
    service = FacturaService(db)
    try:
        factura = service.factura_repo.create_factura(
            id_paciente=paciente_id,
            id_tratamiento=factura_data.id_tratamiento,
            monto_total=factura_data.monto_total,
            monto_pendiente=factura_data.monto_pendiente
        )
        return FacturaResponse.model_validate(factura)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))