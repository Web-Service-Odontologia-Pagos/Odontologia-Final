# app/api/pago_api.py

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db # Usamos get_db definido en app/database.py

# Servicios (descomenta cuando estén listos)
# from app.services.pago_service import PagoService
# from app.services.cambio_estado_service import CambioEstadoService

# Modelos (Domain Layer)
from app.domain.pago_model import (
    PagoRequest, 
    PagoResponse, 
    CambioEPRequest,
    ValidacionPRequest,
    ValidacionPResponse,
    EstadoPago
)

# Inicialización de Routers lógicos para cada HU
router_ipago = APIRouter(tags=["1. Inicio de Pago (HU-21)"])
router_cambio_estado = APIRouter(tags=["2. Gestión de Estado (HU-26, HU-24)"])
router_notificacion = APIRouter(tags=["3. Notificación (HU-23)"])


# ============================================================================
# HU-21: INICIO Y PREPARACIÓN DE PAGO (IPago)
# ============================================================================
@router_ipago.post(
    "/IPago/datosP",
    response_model=PagoResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar Pago",
    description="Recibe datos de la factura y cliente. Valida y retorna estado 'En Proceso'."
)
def iniciar_pago_endpoint(
    pago_data: PagoRequest,
    db: Session = Depends(get_db)
):
    """
    **[HU-21: IPago]** 
    
    Inicia el flujo de pago:
    1. Recibe datos sensibles del cliente (factura, tarjeta, PIN)
    2. Valida que la factura esté 'Pendiente'
    3. Crea un registro de pago con estado 'En Proceso'
    4. Delega al procesador de pagos (EnvioP - HU-25)
    
    **Respuesta:** Estado inicial 'En Proceso'
    
    **Campos requeridos:**
    - `id_factura`: ID de la factura seleccionada
    - `monto_pagado`: Monto a pagar (mayor a 0)
    - `datos_tarjeta`: Número de tarjeta (12-19 dígitos)
    - `pin_seguridad`: CVV/PIN (3-4 dígitos)
    """
    # TODO: Descomenta cuando PagoService esté implementado
    # service = PagoService(db)
    # return service.iniciar_pago(pago_data)
    
    # Respuesta temporal para testing
    return {
        "id": 1,
        "id_factura": pago_data.id_factura,
        "estado_pago": "En Proceso",
        "fecha_inicio": "2025-11-29T00:00:00",
        "id_transaccion_banco": None
    }


# ============================================================================
# HU-26: ACTUALIZACIÓN DEL ESTADO DE PAGO (CambioEP)
# ============================================================================
@router_cambio_estado.put(
    "/paciente/{paciente_id}/cambioEP",
    response_model=PagoResponse,
    status_code=status.HTTP_200_OK,
    summary="Cambiar Estado de Pago",
    description="API interna que actualiza el estado del pago y dispara notificación."
)
def actualizar_estado_pago_endpoint(
    paciente_id: int = Path(..., gt=0, description="ID del paciente propietario del pago"),
    cambio_data: CambioEPRequest = None,
    db: Session = Depends(get_db)
):
    """
    **[HU-26: CambioEP]** 
    
    API interna llamada por ValidaciónP (HU-24).
    
    1. Recibe estado final del banco
    2. Actualiza ATÓMICAMENTE el registro de pago
    3. Dispara NotificacionP (HU-23) al cliente
    4. Actualiza estado de factura si es necesario
    
    **Casos de uso:**
    - Estado = "Pagado": Marcar factura como pagada
    - Estado = "Rechazado": Mantener factura como pendiente
    
    **Campos requeridos:**
    - `id_pago`: ID del pago a actualizar
    - `estado_final`: "Pagado" o "Rechazado"
    - `id_transaccion_banco`: ID de referencia del banco
    """
    # TODO: Descomenta cuando CambioEstadoService esté implementado
    # service = CambioEstadoService(db)
    # return service.actualizar_estado_pago(paciente_id, cambio_data)
    
    if cambio_data is None:
        raise HTTPException(status_code=400, detail="CambioEPRequest es requerido")
    
    # Respuesta temporal para testing
    return {
        "id": cambio_data.id_pago,
        "id_factura": 1,
        "estado_pago": cambio_data.estado_final,
        "fecha_inicio": "2025-11-29T00:00:00",
        "id_transaccion_banco": cambio_data.id_transaccion_banco
    }


# ============================================================================
# HU-24: RECEPCIÓN Y CONFIRMACIÓN DEL ESTADO (ValidaciónP - WEBHOOK)
# ============================================================================
@router_cambio_estado.post(
    "/ValidacionP",
    response_model=ValidacionPResponse,
    status_code=status.HTTP_200_OK,
    summary="Webhook de Validación del Banco",
    description="Endpoint que recibe notificación asíncrona del banco sobre estado de transacción."
)
def webhook_validacion_pago(
    validacion_data: ValidacionPRequest,
    db: Session = Depends(get_db)
):
    """
    **[HU-24: ValidaciónP]** - WEBHOOK ASÍNCRONO
    
    Este es el endpoint que el **banco llamará** cuando la transacción se procese.
    
    **Flujo esperado:**
    1. Cliente inicia pago (HU-21: IPago)
    2. Sistema envía a procesador bancario
    3. Banco procesa y llama a este endpoint (ValidaciónP)
    4. Sistema dispara CambioEP (HU-26) internamente
    5. Sistema dispara NotificacionP (HU-23) al cliente
    
    **Estructura XML equivalente (para referencia de banco):**
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:pag="http://Odontologia.com/pago">
        <soapenv:Header/>
        <soapenv:Body>
            <pag:ValidaciónP>
                <pag:Estado>Pagado</pag:Estado>
                <pag:idTransaccion>ABC123XYZ</pag:idTransaccion>
            </pag:ValidaciónP>
        </soapenv:Body>
    </soapenv:Envelope>
    ```
    
    **Equivalente JSON (para FastAPI):**
    ```json
    {
        "estado": "Pagado",
        "id_transaccion": "ABC123XYZ"
    }
    ```
    
    **Campos requeridos:**
    - `estado`: "Pagado", "Rechazado" o "En Proceso"
    - `id_transaccion`: ID único de la transacción del banco (ej: ABC123XYZ)
    """
    # TODO: Descomenta cuando CambioEstadoService esté implementado
    # service = CambioEstadoService(db)
    # service.actualizar_estado_pago_desde_validacion(validacion_data)
    
    # Respuesta temporal para testing
    return {
        "mensaje": "Estado recibido y actualización interna (CambioEP) disparada con éxito.",
        "id_transaccion": validacion_data.id_transaccion,
        "estado_actualizado": validacion_data.estado
    }


# ============================================================================
# HU-23: NOTIFICACIÓN AL CLIENTE (NotificacionP)
# ============================================================================
@router_notificacion.post(
    "/NotificacionP/pago",
    status_code=status.HTTP_200_OK,
    summary="Notificar Estado de Pago al Cliente",
    description="API interna que notifica al cliente sobre el resultado de su transacción."
)
def notificar_pago_cliente(
    pago_info: PagoResponse,
    db: Session = Depends(get_db)
):
    """
    **[HU-23: NotificacionP]** - API INTERNA
    
    Notifica al cliente sobre el resultado de su pago:
    - Email con confirmación si fue exitoso
    - Email con motivo de rechazo si falló
    
    **Llamada automáticamente por:**
    - CambioEP (HU-26) después de actualizar estado
    
    **Campos:**
    - `id`: ID del pago
    - `id_factura`: ID de la factura
    - `estado_pago`: Estado final
    - `fecha_inicio`: Timestamp de inicio
    - `id_transaccion_banco`: ID de referencia del banco
    """
    # TODO: Implementar envío real de email
    return {
        "mensaje": "Notificación en cola de envío.",
        "id_pago": pago_info.id,
        "email_cliente": "cliente@example.com",
        "asunto": f"Confirmación de Pago - {pago_info.estado_pago}"
    }


# Exportamos todos los routers para ser incluidos en main.py
routers = [router_ipago, router_cambio_estado, router_notificacion]