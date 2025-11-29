# app/config/routers.py

# Importamos los routers de Facturas (HU-22)
from app.api.factura_api import router as factura_router

# Importamos los routers de Pagos (HU-21, HU-26, HU-24, HU-23)
from app.api.pago_api import router_ipago, router_cambio_estado, router_notificacion

# Importamos los routers de Tratamientos
from app.api.tratamiento_api import router as tratamiento_router

# Importamos los routers de Pacientes
from app.api.paciente_api import router as paciente_router

# Lista consolidada de todos los routers de la aplicación
ROUTERS = [
    # Routers de entidades
    paciente_router,
    tratamiento_router,
    
    # Routers de Pagos y Facturas
    factura_router,
    router_ipago,
    router_cambio_estado,
    router_notificacion,
]