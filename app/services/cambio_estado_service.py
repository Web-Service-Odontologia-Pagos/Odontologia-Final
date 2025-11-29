# app/services/cambio_estado_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repository.pago_repository import PagoRepository
from app.domain.pago_model import CambioEPRequest, PagoResponse
import requests # Para simular la llamada a HU-23 (NotificacionP)

class CambioEstadoService:
    """Clase que maneja la lógica de negocio para la actualización de pago (HU-26)."""

    def __init__(self, db: Session):
        self.pago_repo = PagoRepository(db)

    def actualizar_estado_pago(self, data: CambioEPRequest) -> PagoResponse:
        """
        [HU-26: CambioEP] Lógica: Actualiza ATÓMICAMENTE el estado de pago y dispara HU-23.
        """
        
        # 1. Orquestación: Llama al repositorio para la actualización atómica (HU-26)
        # Esto es clave: Se asegura la integridad de los datos en la BD.
        pago_db = self.pago_repo.update_estado_pago_atomico(
            id_pago=data.id_pago,
            estado_final=data.estado_final,
            id_transaccion_banco=data.id_transaccion_banco
        )

        if not pago_db:
            # Manejo de Error: HTTP 404 Not Found si el registro de pago no se encontró (HU-26).
            raise HTTPException(
                status_code=404, 
                detail=f"Registro de pago con ID {data.id_pago} no encontrado para actualizar."
            )

        # 2. Orquestación: Consumir inmediatamente la HU-23 (NotificacionP)
        # El pago ya se actualizó, ahora se notifica al cliente.
        try:
            notificacion_payload = PagoResponse.model_validate(pago_db)
            
            # Simulación de llamada a HU-23 (NotificacionP)
            # requests.post("http://localhost:8000/NotificacionP/pago", json=notificacion_payload.model_dump())
            print(f"Disparando NotificacionP (HU-23) para pago ID: {pago_db.id} con estado {pago_db.estado_pago}")
            pass

        except Exception as e:
            # La falla en la notificación no debe revertir el pago, solo se registra un error.
            print(f"Advertencia: La notificación (HU-23) falló para el pago {pago_db.id}.")
        
        # 3. Mapeo y Respuesta
        return PagoResponse.model_validate(pago_db)