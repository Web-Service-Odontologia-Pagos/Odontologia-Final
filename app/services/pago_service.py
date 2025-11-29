# app/services/pago_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.factura_repository import FacturaRepository
from app.repository.pago_repository import PagoRepository
from app.domain.pago_model import PagoRequest, PagoResponse
import requests # Simulación para la llamada a la HU-25 (EnvioP)

class PagoService:
    """Clase que maneja la lógica de negocio para el inicio del pago (HU-21)."""

    def __init__(self, db: Session):
        self.factura_repo = FacturaRepository(db)
        self.pago_repo = PagoRepository(db)

    def iniciar_pago(self, pago_data: PagoRequest) -> PagoResponse:
        """
        [HU-21: IPago] Lógica: Valida factura, registra pago 'En Proceso' y llama a EnvioP (HU-25).
        """
        factura = self.factura_repo.get_factura_by_id(pago_data.id_factura)

        # 1. Validación de Negocio 1: Factura existe.
        if not factura:
            raise HTTPException(status_code=404, detail="Factura no encontrada para el ID proporcionado.")

        # 2. Validación de Negocio 2: Factura en estado 'Pendiente' (Criterio de Aceptación HU-21).
        if factura.estado_factura != "Pendiente":
            raise HTTPException(
                status_code=400, 
                detail=f"La factura {pago_data.id_factura} no está 'Pendiente' y no puede ser pagada."
            )
            
        # 3. Orquestación y Registro: Creación de registro 'En Proceso' en la BD.
        pago_db = self.pago_repo.create_pago(
            id_factura=pago_data.id_factura,
            monto_pagado=pago_data.monto_pagado
        )

        # 4. Orquestación: Llamada al Módulo Externo (Simulación de HU-25: EnvioP SOAP).
        # En la implementación real, la falla aquí resultaría en HTTP 502 Bad Gateway.
        try:
            # Lógica de conversión a XML y llamada SOAP aquí... (simulada)
            print(f"Llamando a HU-25 (EnvioP) para pago ID: {pago_db.id}")
            pass
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Fallo al comunicar con el módulo bancario (EnvioP).")

        # 5. Mapeo y Respuesta: Devuelve el estado 'En Proceso' al cliente.
        return PagoResponse.model_validate(pago_db)