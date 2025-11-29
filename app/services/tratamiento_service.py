# app/services/tratamiento_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.tratamiento_repository import TratamientoRepository
from app.domain.tratamiento_model import TratamientoResponse
from typing import List


class TratamientoService:
    """Clase que maneja la lógica de negocio para los tratamientos."""

    def __init__(self, db: Session):
        self.tratamiento_repo = TratamientoRepository(db)

    def get_all_tratamientos(self) -> List[TratamientoResponse]:
        """Obtiene la lista de todos los tratamientos."""
        tratamientos = self.tratamiento_repo.get_all_tratamientos()
        return [TratamientoResponse.model_validate(t) for t in tratamientos]

    def get_tratamiento_by_id(self, tratamiento_id: int) -> TratamientoResponse:
        """Obtiene un tratamiento por ID."""
        tratamiento = self.tratamiento_repo.get_tratamiento_by_id(tratamiento_id)
        
        if not tratamiento:
            raise HTTPException(
                status_code=404,
                detail=f"Tratamiento con ID {tratamiento_id} no encontrado."
            )
        
        return TratamientoResponse.model_validate(tratamiento)

    def create_tratamiento(self, nombre: str, costo_total: float) -> TratamientoResponse:
        """Crea un nuevo tratamiento con validaciones."""
        # Validar que el costo sea positivo
        if costo_total <= 0:
            raise HTTPException(
                status_code=400,
                detail="El costo del tratamiento debe ser mayor a 0."
            )
        
        # Crear el tratamiento
        tratamiento = self.tratamiento_repo.create_tratamiento(nombre, costo_total)
        return TratamientoResponse.model_validate(tratamiento)

    def update_tratamiento(self, tratamiento_id: int, nombre: str = None, costo_total: float = None) -> TratamientoResponse:
        """Actualiza un tratamiento existente."""
        # Verificar que el tratamiento existe
        tratamiento = self.tratamiento_repo.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            raise HTTPException(
                status_code=404,
                detail=f"Tratamiento con ID {tratamiento_id} no encontrado."
            )
        
        # Validar que el costo sea positivo si se intenta cambiar
        if costo_total is not None and costo_total <= 0:
            raise HTTPException(
                status_code=400,
                detail="El costo del tratamiento debe ser mayor a 0."
            )
        
        # Actualizar el tratamiento
        tratamiento_actualizado = self.tratamiento_repo.update_tratamiento(tratamiento_id, nombre, costo_total)
        return TratamientoResponse.model_validate(tratamiento_actualizado)

    def delete_tratamiento(self, tratamiento_id: int) -> bool:
        """Elimina un tratamiento."""
        # Verificar que el tratamiento existe
        tratamiento = self.tratamiento_repo.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            raise HTTPException(
                status_code=404,
                detail=f"Tratamiento con ID {tratamiento_id} no encontrado."
            )
        
        return self.tratamiento_repo.delete_tratamiento(tratamiento_id)
