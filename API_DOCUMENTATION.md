# API Web Service de Pagos Odontología

## 📋 Descripción
API RESTful profesional con arquitectura en capas para gestionar un flujo completo de pagos en una clínica odontológica. La aplicación maneja pacientes, tratamientos, facturas y pagos con validaciones y manejo de errores robusto.

---

## 🚀 Inicializar el Proyecto

### Requisitos
- Python 3.11+
- Virtual Environment activado
- Dependencias instaladas: `pip install -r requirements.txt`

### Ejecutar el Servidor

```bash
# Activar entorno virtual
& "C:\Users\Sebastian\Documents\Odontologia Final\Odontologia-Final\venv\Scripts\Activate.ps1"

# Ejecutar servidor con auto-reload
python -m uvicorn app.main:app --reload
```

El servidor estará disponible en: **http://127.0.0.1:8000**

---

## 📚 Documentación Interactiva

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 🔌 Endpoints Disponibles

### 1. **Estado de la Aplicación**
| Método | Ruta | Descripción | Respuesta |
|--------|------|-------------|-----------|
| `GET` | `/` | Verificar que la API está en línea | JSON |
| `GET` | `/health` | Health check | `{"status": "healthy"}` |

---

### 2. **Pacientes** (`/pacientes`)

#### Listar todos los pacientes
```bash
GET /pacientes/
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "3001234567"
  }
]
```

---

#### Obtener un paciente específico
```bash
GET /pacientes/{paciente_id}
```

**Parámetros:**
- `paciente_id` (path): ID del paciente

**Respuesta:**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "3001234567"
}
```

---

#### Crear un nuevo paciente
```bash
POST /pacientes/
```

**Body (JSON):**
```json
{
  "nombre": "María García",
  "email": "maria@example.com",
  "telefono": "3001234567"
}
```

**Validaciones:**
- ✅ Email debe ser único
- ✅ Email debe ser válido
- ✅ Nombre es requerido

**Respuesta (201 Created):**
```json
{
  "id": 2,
  "nombre": "María García",
  "email": "maria@example.com",
  "telefono": "3001234567"
}
```

---

#### Actualizar un paciente
```bash
PUT /pacientes/{paciente_id}
```

**Body (JSON):**
```json
{
  "nombre": "María García Rodríguez",
  "email": "maria.nueva@example.com",
  "telefono": "3009876543"
}
```

**Respuesta (200 OK):**
```json
{
  "id": 2,
  "nombre": "María García Rodríguez",
  "email": "maria.nueva@example.com",
  "telefono": "3009876543"
}
```

---

#### Eliminar un paciente
```bash
DELETE /pacientes/{paciente_id}
```

**Respuesta (204 No Content):** (sin cuerpo)

---

### 3. **Tratamientos** (`/tratamientos`)

#### Listar todos los tratamientos
```bash
GET /tratamientos/
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Limpieza Dental",
    "costo_total": 50000
  }
]
```

---

#### Obtener un tratamiento específico
```bash
GET /tratamientos/{tratamiento_id}
```

**Respuesta:**
```json
{
  "id": 1,
  "nombre": "Limpieza Dental",
  "costo_total": 50000
}
```

---

#### Crear un nuevo tratamiento
```bash
POST /tratamientos/
```

**Body (JSON):**
```json
{
  "nombre": "Ortodoncia",
  "costo_total": 2000000
}
```

**Validaciones:**
- ✅ Nombre es requerido
- ✅ Costo debe ser > 0

**Respuesta (201 Created):**
```json
{
  "id": 2,
  "nombre": "Ortodoncia",
  "costo_total": 2000000
}
```

---

#### Actualizar un tratamiento
```bash
PUT /tratamientos/{tratamiento_id}
```

**Body (JSON):**
```json
{
  "nombre": "Ortodoncia Avanzada",
  "costo_total": 2500000
}
```

**Respuesta (200 OK):**
```json
{
  "id": 2,
  "nombre": "Ortodoncia Avanzada",
  "costo_total": 2500000
}
```

---

#### Eliminar un tratamiento
```bash
DELETE /tratamientos/{tratamiento_id}
```

**Respuesta (204 No Content):** (sin cuerpo)

---

### 4. **Facturas** (`/usuarios/{paciente_id}/consultaF`)

#### Consultar facturas pendientes de un paciente (HU-22)
```bash
GET /usuarios/{paciente_id}/consultaF
```

**Parámetros:**
- `paciente_id` (path): ID del paciente

**Respuesta:**
```json
[
  {
    "id": 1,
    "id_paciente": 1,
    "id_tratamiento": 1,
    "monto_total": 500000,
    "monto_pendiente": 500000,
    "estado_factura": "Pendiente",
    "fecha_creacion": "2025-11-29T10:30:00"
  }
]
```

**Estados posibles:**
- `Pendiente` - Factura no pagada
- `Pagada` - Factura pagada
- `Cancelada` - Factura cancelada

---

### 5. **Pagos** (En construcción - comentados)

Los endpoints de pagos están comentados temporalmente mientras se completan los servicios:

- `POST /IPago/datosP` - Iniciar pago (HU-21)
- `PUT /paciente/{paciente_id}/cambioEP` - Cambio de estado de pago (HU-26)
- `POST /ValidacionP` - Webhook de validación (HU-24)
- `POST /NotificacionP/pago` - Notificación de pago (HU-23)

---

## 🏗️ Estructura de Capas

```
app/
├── api/                      # Capa de Presentación (Endpoints)
│   ├── paciente_api.py
│   ├── tratamiento_api.py
│   ├── factura_api.py
│   └── pago_api.py
├── services/                 # Capa de Lógica de Negocio
│   ├── paciente_service.py
│   ├── tratamiento_service.py
│   ├── factura_service.py
│   ├── pago_service.py
│   └── cambio_estado_service.py
├── repository/               # Capa de Acceso a Datos
│   ├── paciente_repository.py
│   ├── tratamiento_repository.py
│   ├── factura_repository.py
│   └── pago_repository.py
├── models/                   # Modelos ORM (SQLAlchemy)
│   ├── pacientes_db.py
│   ├── tratamiento_db.py
│   ├── factura_db.py
│   └── pago_db.py
├── domain/                   # Modelos Pydantic (Validación)
│   ├── paciente_model.py
│   ├── tratamiento_model.py
│   ├── factura_model.py
│   └── pago_model.py
├── config/
│   └── routers.py           # Registro centralizado de routers
├── database.py              # Configuración de BD
└── main.py                  # Aplicación principal
```

---

## ✅ Características Implementadas

- ✅ **Pacientes**: CRUD completo con validación de emails únicos
- ✅ **Tratamientos**: CRUD completo con validación de costos positivos
- ✅ **Facturas**: Consulta de facturas pendientes por paciente
- ✅ **Arquitectura en capas**: Separación clara de responsabilidades
- ✅ **Validación de datos**: Con Pydantic models
- ✅ **Manejo de errores**: Excepciones HTTP correctas
- ✅ **Documentación automática**: Swagger UI y ReDoc
- ✅ **Base de datos**: SQLite con SQLAlchemy ORM

---

## 🔒 Manejo de Errores

Todos los endpoints incluyen validaciones y devuelven errores apropiados:

```json
{
  "detail": "Paciente con ID 999 no encontrado."
}
```

**Códigos HTTP utilizados:**
- `200 OK` - Operación exitosa
- `201 Created` - Recurso creado
- `204 No Content` - Eliminación exitosa
- `400 Bad Request` - Datos inválidos
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

---

## 📝 Notas Importantes

1. **Base de datos**: Se crea automáticamente al iniciar (`odontologia_db.db`)
2. **Requerimientos**: Instalar con `pip install -r requirements.txt`
3. **Email único**: Los pacientes no pueden compartir email
4. **Costos positivos**: Los tratamientos deben tener costo > 0

---

## 🔄 Proximos Pasos

- [ ] Implementar endpoints de pagos
- [ ] Integración con pasarela bancaria
- [ ] Autenticación y autorización
- [ ] Tests unitarios
- [ ] Logs y monitoreo
- [ ] Documentación en PDF

---

**Última actualización:** 29 de Noviembre de 2025
**Versión:** 1.0.0
