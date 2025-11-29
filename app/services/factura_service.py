# app/services/factura_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.factura_repository import FacturaRepository
from app.repository.paciente_repository import PacienteRepository
from app.domain.factura_model import FacturaResponse
from typing import List

class FacturaService:
    """Clase que maneja la lógica de negocio para la consulta de facturas (HU-22)."""

    def __init__(self, db: Session):
        # Inicializa los repositorios necesarios
        self.factura_repo = FacturaRepository(db)
        self.paciente_repo = PacienteRepository(db)
    
    def get_facturas_pendientes_by_paciente(self, paciente_id: int) -> List[FacturaResponse]:
        """
        [HU-22: ConsultaF] Lógica: Valida el paciente y consulta solo las facturas pendientes.
        """
        # 1. Validación de Negocio: Verificar que el paciente exista (Criterio de Aceptación)
        paciente = self.paciente_repo.get_paciente_by_id(paciente_id)
        
        if not paciente:
            # Manejo de Error: HTTP 404 Not Found si el ID del paciente no existe.
            raise HTTPException(
                status_code=404, 
                detail=f"Paciente con ID {paciente_id} no encontrado."
            )
            
        # 2. Orquestación: Llama al repositorio para aplicar el filtro 'Pendiente'.
        facturas_db = self.factura_repo.get_facturas_pendientes_by_paciente(paciente_id)
        
        # 3. Mapeo: Convierte los objetos FacturaDB a FacturaResponse (Pydantic).
        return [FacturaResponse.model_validate(factura) for factura in facturas_db]