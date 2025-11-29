# app/main.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# ✅ Importación correcta: importación absoluta
from app.config.routers import ROUTERS

# Lógica de Inicialización de Base de Datos
from app.database import create_tables

# Importaciones ORM necesarias (para que el ORM registre los modelos)
import app.models.pacientes_db
import app.models.tratamiento_db
import app.models.factura_db
import app.models.pago_db

# ✅ Mejor práctica: crear tablas en evento de startup
# (evita que se ejecute en cada import y bloqueé procesos)
# ----------------------------------------------------
app = FastAPI(
    title="Web Service de Pagos Odontología",
    description="API con arquitectura en capas para el flujo de pagos (HU-21 a HU-26)",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    create_tables()
# ----------------------------------------------------


# Registra TODOS los routers automáticamente
for router in ROUTERS:
    app.include_router(router)


# Endpoint raíz
@app.get("/", tags=["Estado"])
async def root():
    return {
        "message": "Web Service de Pagos Odontología está en línea.",
        "status": "online",
        "version": "1.0.0"
    }


# Health check
@app.get("/health", tags=["Estado"])
async def health_check():
    return {"status": "healthy"}
