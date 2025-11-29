# app/api/tratamiento_api.py

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.tratamiento_service import TratamientoService
from app.domain.tratamiento_model import TratamientoResponse
from pydantic import BaseModel, Field
from typing import List

# Modelos Pydantic para request
class TratamientoRequest(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del tratamiento")
    costo_total: float = Field(..., gt=0, description="Costo del tratamiento (mayor a 0)")

class TratamientoUpdate(BaseModel):
    nombre: str = Field(None, min_length=1, description="Nombre del tratamiento")
    costo_total: float = Field(None, gt=0, description="Costo del tratamiento (mayor a 0)")

# Router para la gestión de tratamientos
router = APIRouter(prefix="/tratamientos", tags=["Tratamientos"])


@router.get(
    "/",
    response_model=List[TratamientoResponse],
    status_code=status.HTTP_200_OK,
)
def listar_tratamientos(db: Session = Depends(get_db)):
    """
    Lista todos los tratamientos disponibles.
    """
    service = TratamientoService(db)
    return service.get_all_tratamientos()


@router.get(
    "/{tratamiento_id}",
    response_model=TratamientoResponse,
    status_code=status.HTTP_200_OK,
)
def obtener_tratamiento(
    tratamiento_id: int = Path(..., description="ID del tratamiento a consultar."),
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de un tratamiento específico.
    """
    service = TratamientoService(db)
    return service.get_tratamiento_by_id(tratamiento_id)


@router.post(
    "/",
    response_model=TratamientoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_tratamiento(
    tratamiento_data: TratamientoRequest,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo tratamiento.
    """
    service = TratamientoService(db)
    return service.create_tratamiento(
        nombre=tratamiento_data.nombre,
        costo_total=tratamiento_data.costo_total
    )


@router.put(
    "/{tratamiento_id}",
    response_model=TratamientoResponse,
    status_code=status.HTTP_200_OK,
)
def actualizar_tratamiento(
    tratamiento_id: int = Path(..., description="ID del tratamiento a actualizar."),
    tratamiento_data: TratamientoUpdate = None,
    db: Session = Depends(get_db)
):
    """
    Actualiza los detalles de un tratamiento.
    """
    service = TratamientoService(db)
    return service.update_tratamiento(
        tratamiento_id=tratamiento_id,
        nombre=tratamiento_data.nombre if tratamiento_data and tratamiento_data.nombre else None,
        costo_total=tratamiento_data.costo_total if tratamiento_data and tratamiento_data.costo_total else None
    )


@router.delete(
    "/{tratamiento_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_tratamiento(
    tratamiento_id: int = Path(..., description="ID del tratamiento a eliminar."),
    db: Session = Depends(get_db)
):
    """
    Elimina un tratamiento.
    """
    service = TratamientoService(db)
    service.delete_tratamiento(tratamiento_id)
    return None
