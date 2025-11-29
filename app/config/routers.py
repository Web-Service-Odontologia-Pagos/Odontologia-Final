# app/config/routers.py

# Importamos los routers de Facturas (HU-22)
from app.api.factura_api import router as factura_router

# Importamos los routers de Pagos (HU-21, HU-26, HU-24, HU-23)
from app.api.pago_api import router_ipago, router_cambio_estado, router_notificacion

# Si tenías un router de usuarios previo:
# from app.api.user_api import router as user_router 

# Lista consolidada de todos los routers de la aplicación
ROUTERS = [
    # Routers de Pagos y Facturas
    factura_router,
    router_ipago,
    router_cambio_estado,
    router_notificacion,
    
    # Aquí irían otros routers que ya tenías (ej: user_router)
]