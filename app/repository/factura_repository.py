# app/repository/factura_repository.py

from sqlalchemy.orm import Session
from app.models.factura_db import FacturaDB # Importa el modelo de la tabla Facturas
from app.models.paciente_db import PacienteDB # Para consultas consolidadas

class FacturaRepository:
    """Clase que maneja todas las operaciones CRUD para la tabla 'facturas'."""
    
    def __init__(self, db: Session):
        # Constructor: recibe una sesión de base de datos
        self.db = db

    def get_facturas_pendientes_by_paciente(self, paciente_id: int) -> list[FacturaDB]:
        """
        Consulta todas las facturas del paciente en estado 'Pendiente' (HU-22).
        
        Args:
            paciente_id: ID del paciente a consultar.
        
        Returns:
            Lista de objetos FacturaDB que cumplen con el filtro.
        """
        return (
            self.db.query(FacturaDB)
            # Join opcional para asegurar que el paciente exista
            .join(PacienteDB, FacturaDB.id_paciente == PacienteDB.id)
            .filter(
                FacturaDB.id_paciente == paciente_id,
                FacturaDB.estado_factura == "Pendiente" # Lógica clave de HU-22
            )
            .all()
        )

    def get_factura_by_id(self, factura_id: int) -> FacturaDB | None:
        """
        Busca una factura por ID (necesario para validación en HU-21).
        """
        return self.db.query(FacturaDB).filter(FacturaDB.id == factura_id).first()