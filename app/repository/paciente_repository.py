# app/repository/paciente_repository.py

from sqlalchemy.orm import Session
from app.models.pacientes_db import PacienteDB
from typing import List, Optional


class PacienteRepository:
    """Clase que maneja todas las operaciones CRUD para la tabla 'pacientes'."""

    def __init__(self, db: Session):
        self.db = db

    def get_all_pacientes(self) -> List[PacienteDB]:
        """Obtiene todos los pacientes registrados."""
        return self.db.query(PacienteDB).all()

    def get_paciente_by_id(self, paciente_id: int) -> Optional[PacienteDB]:
        """Busca un paciente por ID (necesario para validación y datos de contacto en HU-23)."""
        return self.db.query(PacienteDB).filter(PacienteDB.id == paciente_id).first()

    def get_paciente_by_email(self, email: str) -> Optional[PacienteDB]:
        """Busca un paciente por email (para validar duplicados)."""
        return self.db.query(PacienteDB).filter(PacienteDB.email == email).first()

    def create_paciente(self, nombre: str, email: str, telefono: str = None) -> PacienteDB:
        """Crea un nuevo paciente."""
        paciente = PacienteDB(
            nombre=nombre,
            email=email,
            telefono=telefono
        )
        self.db.add(paciente)
        self.db.commit()
        self.db.refresh(paciente)
        return paciente

    def update_paciente(self, paciente_id: int, nombre: str = None, email: str = None, telefono: str = None) -> Optional[PacienteDB]:
        """Actualiza un paciente existente."""
        paciente = self.db.query(PacienteDB).filter(PacienteDB.id == paciente_id).first()
        
        if paciente:
            if nombre is not None:
                paciente.nombre = nombre
            if email is not None:
                paciente.email = email
            if telefono is not None:
                paciente.telefono = telefono
            
            self.db.commit()
            self.db.refresh(paciente)
        
        return paciente

    def delete_paciente(self, paciente_id: int) -> bool:
        """Elimina un paciente por ID."""
        paciente = self.db.query(PacienteDB).filter(PacienteDB.id == paciente_id).first()
        
        if paciente:
            self.db.delete(paciente)
            self.db.commit()
            return True
        
        return False

    