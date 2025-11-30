# app/main.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import logging
import logging.config
import sys

# Configuración centralizada de logging (incluye uvicorn y sqlalchemy)
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(correlation_id)s | %(message)s"
LOG_LEVEL = "INFO"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": LOG_FORMAT},
    },
    "filters": {
        "correlation": {"()": "app.middleware.correlation.CorrelationIdFilter"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
            "filters": ["correlation"],
            "level": LOG_LEVEL,
        }
    },
    "loggers": {
        "": {"handlers": ["console"], "level": LOG_LEVEL},
        "odontologia": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "uvicorn": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "uvicorn.error": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "uvicorn.access": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "sqlalchemy": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "sqlalchemy.engine": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("odontologia")
logger.info("Logger inicializado para Odontologia Web Service (integrado uvicorn/sqlalchemy)")

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

# Registrar middleware de correlation id
from app.middleware.correlation import CorrelationIdMiddleware
app.add_middleware(CorrelationIdMiddleware)

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
