# app/api/pago_api.py

from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session
from app.database import get_db # Usamos get_db definido en app/database.py

# TODO: Descomenta cuando los servicios estén correctamente configurados
# Servicios
# from app.services.pago_service import PagoService
# from app.services.cambio_estado_service import CambioEstadoService

# Modelos (Domain Layer)
# from app.domain.pago_model import PagoRequest, PagoResponse, CambioEPRequest

# Inicialización de Routers lógicos para cada HU
router_ipago = APIRouter(tags=["1. Inicio de Pago (HU-21)"])
router_cambio_estado = APIRouter(tags=["2. Gestión de Estado (HU-26, HU-24)"])
router_notificacion = APIRouter(tags=["3. Notificación (HU-23)"])


# TODO: Descomenta los endpoints cuando los servicios estén configurados correctamente
# Los endpoints han sido comentados temporalmente para evitar errores de importación

# # --- HU-21: INICIO Y PREPARACIÓN DE PAGO (IPago) ---
# @router_ipago.post(
#     "/IPago/datosP", # Ruta definida en HU-21
#     response_model=PagoResponse,
#     status_code=status.HTTP_200_OK,
# )
# def iniciar_pago_endpoint(
#     pago_data: PagoRequest, # Los datos del cliente validados por Pydantic
#     db: Session = Depends(get_db)
# ):
#     """
#     [HU-21: IPago] 
#     Recibe datos sensibles, valida que la factura esté 'Pendiente' y delega 
#     el proceso a EnvioP (HU-25).
#     Respuesta: Estado 'En Proceso'.
#     """
#     service = PagoService(db)
#     return service.iniciar_pago(pago_data)

# # --- HU-26: ACTUALIZACIÓN DEL ESTADO DE PAGO (CambioEP) ---
# @router_cambio_estado.put(
#     "/paciente/{paciente_id}/cambioEP", # Ruta definida en HU-26
#     response_model=PagoResponse,
#     status_code=status.HTTP_200_OK,
# )
# def actualizar_estado_pago_endpoint(
#     paciente_id: int = Path(..., description="ID del paciente. Requerido por la estructura de la ruta."), 
#     cambio_data: CambioEPRequest = None,
#     db: Session = Depends(get_db)
# ):
#     """
#     [HU-26: CambioEP] 
#     API interna. Recibe el estado final del banco y actualiza ATÓMICAMENTE el 
#     registro de pago. Dispara NotificacionP (HU-23).
#     """
#     service = CambioEstadoService(db)
#     return service.actualizar_estado_pago(cambio_data)

# # --- HU-24: RECEPCIÓN Y CONFIRMACIÓN DEL ESTADO (ValidaciónP) ---
# @router_cambio_estado.post(
#     "/ValidacionP", # Endpoint de Webhook definido en HU-24
#     status_code=status.HTTP_200_OK,
# )
# def webhook_validacion_pago(
#     cambio_data: CambioEPRequest,
#     db: Session = Depends(get_db)
# ):
#     """
#     [HU-24: ValidaciónP] 
#     Simula el Webhook Asíncrono del banco.
#     """
#     service = CambioEstadoService(db)
#     service.actualizar_estado_pago(cambio_data)
#     return {"message": "Estado recibido y actualización interna (CambioEP) disparada con éxito."}

# # --- HU-23: NOTIFICACIÓN AL CLIENTE (NotificacionP) ---
# @router_notificacion.post(
#     "/NotificacionP/pago",
#     status_code=status.HTTP_200_OK,
# )
# def notificar_pago_cliente(
#     pago_info: PagoResponse,
#     db: Session = Depends(get_db)
# ):
#     """
#     [HU-23: NotificacionP] 
#     API interna (consumida por HU-26).
#     """
#     return {"message": "Notificación en cola de envío."}

# Exportamos todos los routers para ser incluidos en main.py
routers = [router_ipago, router_cambio_estado, router_notificacion]