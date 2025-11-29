# 🏥 Web Service de Pagos - Odontología

[![FastAPI](https://img.shields.io/badge/FastAPI-0.122.0-green)]()
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.44-blue)]()
[![Python](https://img.shields.io/badge/Python-3.11+-purple)]()

Solución profesional de API RESTful para gestionar facturas y pagos en una clínica odontológica.

---

## 🎯 Características Principales

### ✅ Funcionalidades Implementadas
- **CRUD de Pacientes**: Crear, leer, actualizar y eliminar pacientes
- **CRUD de Tratamientos**: Gestión completa de tratamientos disponibles
- **Consulta de Facturas**: Obtener facturas pendientes por paciente (HU-22)
- **Arquitectura en Capas**: API → Service → Repository → Database
- **Validaciones Automáticas**: Con Pydantic
- **Documentación Interactiva**: Swagger UI incluida

### 🔄 En Desarrollo
- Sistema de Pagos (HU-21, HU-23, HU-24, HU-26)
- Integración bancaria
- Autenticación

---

## ⚡ Inicio Rápido

### 1️⃣ Requisitos
```bash
# Python 3.11 o superior
python --version

# Pip
pip --version
```

### 2️⃣ Clonar y Configurar
```bash
# Navegar al directorio
cd "C:\Users\Sebastian\Documents\Odontologia Final\Odontologia-Final"

# Crear virtual environment (si no existe)
python -m venv venv

# Activar virtual environment (PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 3️⃣ Ejecutar Servidor
```bash
python -m uvicorn app.main:app --reload
```

### 4️⃣ Acceder a la API
- **Aplicación**: http://127.0.0.1:8000
- **Documentación Swagger**: http://127.0.0.1:8000/docs
- **Documentación ReDoc**: http://127.0.0.1:8000/redoc
- **Health Check**: http://127.0.0.1:8000/health

---

## 📚 Ejemplos de Uso

### Crear un Paciente
```bash
curl -X POST "http://127.0.0.1:8000/pacientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "3001234567"
  }'
```

### Crear un Tratamiento
```bash
curl -X POST "http://127.0.0.1:8000/tratamientos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Limpieza Dental",
    "costo_total": 50000
  }'
```

### Obtener Facturas Pendientes
```bash
curl -X GET "http://127.0.0.1:8000/usuarios/1/consultaF"
```

---

## 🗂️ Estructura del Proyecto

```
Odontologia-Final/
├── app/
│   ├── api/                    # Endpoints
│   │   ├── paciente_api.py
│   │   ├── tratamiento_api.py
│   │   ├── factura_api.py
│   │   └── pago_api.py
│   ├── services/              # Lógica de negocio
│   │   ├── paciente_service.py
│   │   ├── tratamiento_service.py
│   │   └── ...
│   ├── repository/            # Acceso a datos
│   │   ├── paciente_repository.py
│   │   ├── tratamiento_repository.py
│   │   └── ...
│   ├── models/                # Modelos ORM
│   │   ├── pacientes_db.py
│   │   ├── tratamiento_db.py
│   │   └── ...
│   ├── domain/                # Modelos Pydantic
│   │   ├── paciente_model.py
│   │   ├── tratamiento_model.py
│   │   └── ...
│   ├── config/
│   │   └── routers.py
│   ├── database.py
│   ├── main.py
│   └── __init__.py
├── requirements.txt
├── .env                       # Variables de entorno (crear si falta)
├── .gitignore
├── API_DOCUMENTATION.md       # Documentación detallada
└── README.md                  # Este archivo
```

---

## 🔌 API Endpoints

| Método | Ruta | Descripción | Status |
|--------|------|-------------|--------|
| `GET` | `/` | Estado de la API | ✅ |
| `GET` | `/health` | Health check | ✅ |
| **PACIENTES** |
| `GET` | `/pacientes/` | Listar pacientes | ✅ |
| `GET` | `/pacientes/{id}` | Obtener paciente | ✅ |
| `POST` | `/pacientes/` | Crear paciente | ✅ |
| `PUT` | `/pacientes/{id}` | Actualizar paciente | ✅ |
| `DELETE` | `/pacientes/{id}` | Eliminar paciente | ✅ |
| **TRATAMIENTOS** |
| `GET` | `/tratamientos/` | Listar tratamientos | ✅ |
| `GET` | `/tratamientos/{id}` | Obtener tratamiento | ✅ |
| `POST` | `/tratamientos/` | Crear tratamiento | ✅ |
| `PUT` | `/tratamientos/{id}` | Actualizar tratamiento | ✅ |
| `DELETE` | `/tratamientos/{id}` | Eliminar tratamiento | ✅ |
| **FACTURAS** |
| `GET` | `/usuarios/{id}/consultaF` | Facturas pendientes | ✅ |
| **PAGOS** |
| `POST` | `/IPago/datosP` | Iniciar pago | 🔧 |
| `PUT` | `/paciente/{id}/cambioEP` | Cambio de estado | 🔧 |
| `POST` | `/ValidacionP` | Webhook | 🔧 |
| `POST` | `/NotificacionP/pago` | Notificación | 🔧 |

---

## 📖 Documentación Completa

Para una documentación detallada de todos los endpoints, parámetros y respuestas, consulta:
- **`API_DOCUMENTATION.md`** - Documentación completa con ejemplos

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validación de datos
- **SQLite** - Base de datos
- **Uvicorn** - Servidor ASGI
- **Python 3.11+** - Lenguaje

---

## ⚙️ Configuración

### Variables de Entorno (`.env`)
```bash
# DATABASE
DATABASE_URL=sqlite:///./odontologia_db.db

# API
API_TITLE=Web Service de Pagos Odontología
API_VERSION=1.0.0
```

### Base de Datos
La base de datos se crea automáticamente al iniciar la aplicación:
```
odontologia_db.db
```

---

## 🧪 Testing

### Probar con cURL

```bash
# Listar pacientes
curl http://127.0.0.1:8000/pacientes/

# Probar health check
curl http://127.0.0.1:8000/health
```

### Probar con Swagger UI
1. Accede a http://127.0.0.1:8000/docs
2. Click en un endpoint
3. Click en "Try it out"
4. Ajusta los parámetros
5. Click en "Execute"

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
# Asegúrate de activar el virtual environment
.\venv\Scripts\Activate.ps1
```

### Error: "Port 8000 already in use"
```bash
# Usar otro puerto
python -m uvicorn app.main:app --port 8001 --reload
```

### Error: "Database locked"
```bash
# Eliminar la BD y dejar que se recree
Remove-Item odontologia_db.db -Force
```

---

## 📝 Próximas Mejoras

- [ ] Autenticación JWT
- [ ] Tests unitarios y e2e
- [ ] Rate limiting
- [ ] Paginación
- [ ] Filtros avanzados
- [ ] Logs estructurados
- [ ] Deploy en producción
- [ ] CI/CD pipeline

---

## 📧 Contacto y Soporte

Para reportar issues o sugerencias:
1. Crear un GitHub issue
2. Describir el problema
3. Incluir pasos para reproducir

---

## 📄 Licencia

Este proyecto es propiedad de Web Service Odontología.

---

**Última actualización:** 29 de Noviembre de 2025  
**Versión:** 1.0.0
