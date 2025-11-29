# app/repository/paciente_repository.py

from sqlalchemy.orm import Session
from app.models.paciente_db import PacienteDB # Importa el modelo de la tabla Pacientes

class PacienteRepository:
    """Clase que maneja las operaciones de la tabla 'pacientes'."""

    def __init__(self, db: Session):
        self.db = db

    def get_paciente_by_id(self, paciente_id: int) -> PacienteDB | None:
        """
        Busca un paciente por ID (necesario para validación y datos de contacto en HU-23).
        """
        return self.db.query(PacienteDB).filter(PacienteDB.id == paciente_id).first()
    