# app/config/routers.py

# Importaciones de routers para el flujo de pagos
from app.api import factura_api 
from app.api import pago_api 

# Lista de todos los routers que se registrarán en la aplicación
ROUTERS = [
    # Routers del Flujo de Pagos
    factura_api.router,
    pago_api.router_ipago, 
    pago_api.router_cambio_estado, 
    pago_api.router_notificacion,
]