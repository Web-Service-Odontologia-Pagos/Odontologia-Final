# app/api/factura_api.py

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session
from app.database import get_db # Función de dependencia para la sesión de BD

# TODO: Descomenta cuando los servicios estén correctamente configurados
# from app.services.factura_service import FacturaService
# from app.domain.factura_model import FacturaResponse
from typing import List

# Router para la gestión de facturas.
# Ruta definida en HU-22: /usuarios/{id}/consultaF
router = APIRouter(prefix="/usuarios", tags=["Facturas (HU-22)"])

@router.get(
    "/{paciente_id}/consultaF",
    # response_model=List[FacturaResponse],
    status_code=status.HTTP_200_OK,
)
def get_facturas_pendientes_endpoint(
    paciente_id: int = Path(..., description="ID del paciente a consultar."),
    db: Session = Depends(get_db) # Inyección de la sesión de BD
):
    """
    [HU-22: ConsultaF] 
    Devuelve la lista consolidada de facturas en estado 'Pendiente' para un paciente.
    """
    # TODO: Implementar la lógica del servicio
    # service = FacturaService(db)
    # return service.get_facturas_pendientes_by_paciente(paciente_id)
    
    # Respuesta temporal para pruebas
    return {"mensaje": "Endpoint de facturas en construcción", "paciente_id": paciente_id}