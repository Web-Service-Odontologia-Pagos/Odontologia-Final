# app/api/paciente_api.py

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.paciente_service import PacienteService
from app.domain.paciente_model import PacienteResponse, PacienteBase
from typing import List

# Router para la gestión de pacientes
router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get(
    "/",
    response_model=List[PacienteResponse],
    status_code=status.HTTP_200_OK,
)
def listar_pacientes(db: Session = Depends(get_db)):
    """
    Lista todos los pacientes registrados.
    """
    service = PacienteService(db)
    return service.get_all_pacientes()


@router.get(
    "/{paciente_id}",
    response_model=PacienteResponse,
    status_code=status.HTTP_200_OK,
)
def obtener_paciente(
    paciente_id: int = Path(..., description="ID del paciente a consultar."),
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de un paciente específico.
    """
    service = PacienteService(db)
    return service.get_paciente_by_id(paciente_id)


@router.post(
    "/",
    response_model=PacienteResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_paciente(
    paciente_data: PacienteBase,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo paciente.
    """
    service = PacienteService(db)
    return service.create_paciente(
        nombre=paciente_data.nombre,
        email=paciente_data.email,
        telefono=paciente_data.telefono
    )


@router.put(
    "/{paciente_id}",
    response_model=PacienteResponse,
    status_code=status.HTTP_200_OK,
)
def actualizar_paciente(
    paciente_id: int = Path(..., description="ID del paciente a actualizar."),
    paciente_data: PacienteBase = None,
    db: Session = Depends(get_db)
):
    """
    Actualiza los detalles de un paciente.
    """
    service = PacienteService(db)
    return service.update_paciente(
        paciente_id=paciente_id,
        nombre=paciente_data.nombre if paciente_data else None,
        email=paciente_data.email if paciente_data else None,
        telefono=paciente_data.telefono if paciente_data else None
    )


@router.delete(
    "/{paciente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_paciente(
    paciente_id: int = Path(..., description="ID del paciente a eliminar."),
    db: Session = Depends(get_db)
):
    """
    Elimina un paciente.
    """
    service = PacienteService(db)
    service.delete_paciente(paciente_id)
    return None
