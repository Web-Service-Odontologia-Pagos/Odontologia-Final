# app/services/paciente_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.paciente_repository import PacienteRepository
from app.domain.paciente_model import PacienteResponse
from typing import List


class PacienteService:
    """Clase que maneja la lógica de negocio para los pacientes."""

    def __init__(self, db: Session):
        self.paciente_repo = PacienteRepository(db)

    def get_all_pacientes(self) -> List[PacienteResponse]:
        """Obtiene la lista de todos los pacientes."""
        pacientes = self.paciente_repo.get_all_pacientes()
        return [PacienteResponse.model_validate(p) for p in pacientes]

    def get_paciente_by_id(self, paciente_id: int) -> PacienteResponse:
        """Obtiene un paciente por ID."""
        paciente = self.paciente_repo.get_paciente_by_id(paciente_id)
        
        if not paciente:
            raise HTTPException(
                status_code=404,
                detail=f"Paciente con ID {paciente_id} no encontrado."
            )
        
        return PacienteResponse.model_validate(paciente)

    def create_paciente(self, nombre: str, email: str, telefono: str = None) -> PacienteResponse:
        """Crea un nuevo paciente con validaciones."""
        # Validar que el email no esté duplicado
        paciente_existente = self.paciente_repo.get_paciente_by_email(email)
        if paciente_existente:
            raise HTTPException(
                status_code=400,
                detail=f"El email {email} ya está registrado."
            )
        
        # Crear el paciente
        paciente = self.paciente_repo.create_paciente(nombre, email, telefono)
        return PacienteResponse.model_validate(paciente)

    def update_paciente(self, paciente_id: int, nombre: str = None, email: str = None, telefono: str = None) -> PacienteResponse:
        """Actualiza un paciente existente."""
        # Verificar que el paciente existe
        paciente = self.paciente_repo.get_paciente_by_id(paciente_id)
        if not paciente:
            raise HTTPException(
                status_code=404,
                detail=f"Paciente con ID {paciente_id} no encontrado."
            )
        
        # Si se intenta cambiar el email, validar que no esté duplicado
        if email and email != paciente.email:
            paciente_existente = self.paciente_repo.get_paciente_by_email(email)
            if paciente_existente:
                raise HTTPException(
                    status_code=400,
                    detail=f"El email {email} ya está registrado."
                )
        
        # Actualizar el paciente
        paciente_actualizado = self.paciente_repo.update_paciente(paciente_id, nombre, email, telefono)
        return PacienteResponse.model_validate(paciente_actualizado)

    def delete_paciente(self, paciente_id: int) -> bool:
        """Elimina un paciente."""
        # Verificar que el paciente existe
        paciente = self.paciente_repo.get_paciente_by_id(paciente_id)
        if not paciente:
            raise HTTPException(
                status_code=404,
                detail=f"Paciente con ID {paciente_id} no encontrado."
            )
        
        return self.paciente_repo.delete_paciente(paciente_id)
