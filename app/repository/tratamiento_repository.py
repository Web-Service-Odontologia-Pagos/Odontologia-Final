# app/repository/tratamiento_repository.py

from sqlalchemy.orm import Session
from app.models.tratamiento_db import TratamientoDB
from typing import List, Optional


class TratamientoRepository:
    """Clase que maneja todas las operaciones CRUD para la tabla 'tratamientos'."""
    
    def __init__(self, db: Session):
        self.db = db

    def get_all_tratamientos(self) -> List[TratamientoDB]:
        """Obtiene todos los tratamientos."""
        return self.db.query(TratamientoDB).all()

    def get_tratamiento_by_id(self, tratamiento_id: int) -> Optional[TratamientoDB]:
        """Obtiene un tratamiento por ID."""
        return self.db.query(TratamientoDB).filter(TratamientoDB.id == tratamiento_id).first()

    def create_tratamiento(self, nombre: str, costo_total: float) -> TratamientoDB:
        """Crea un nuevo tratamiento."""
        tratamiento = TratamientoDB(
            nombre=nombre,
            costo_total=costo_total
        )
        self.db.add(tratamiento)
        self.db.commit()
        self.db.refresh(tratamiento)
        return tratamiento

    def update_tratamiento(self, tratamiento_id: int, nombre: str = None, costo_total: float = None) -> Optional[TratamientoDB]:
        """Actualiza un tratamiento existente."""
        tratamiento = self.db.query(TratamientoDB).filter(TratamientoDB.id == tratamiento_id).first()
        
        if tratamiento:
            if nombre is not None:
                tratamiento.nombre = nombre
            if costo_total is not None:
                tratamiento.costo_total = costo_total
            
            self.db.commit()
            self.db.refresh(tratamiento)
        
        return tratamiento

    def delete_tratamiento(self, tratamiento_id: int) -> bool:
        """Elimina un tratamiento por ID."""
        tratamiento = self.db.query(TratamientoDB).filter(TratamientoDB.id == tratamiento_id).first()
        
        if tratamiento:
            self.db.delete(tratamiento)
            self.db.commit()
            return True
        
        return False
