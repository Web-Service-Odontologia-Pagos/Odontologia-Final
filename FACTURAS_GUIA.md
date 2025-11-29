# 📊 Guía de Facturas y Consulta de Saldos (HU-22)

## 1. Estructura JSON - Consulta de Saldos

La estructura que proporcionaste es **PERFECTA** para HU-22. La he adoptado completamente en el sistema.

### ✅ Respuesta de ConsultaF (HU-22)

```json
{
  "mensaje": "Consulta de saldos exitosa",
  "data": {
    "fecha_proceso": "2025-11-29",
    "capital_total": 8500000,
    "intereses_causados": 2400000,
    "intereses_contingentes": 1200000,
    "detalle_facturas": [
      {
        "id_factura": 101,
        "monto": 4500000,
        "monto_pendiente": 4500000,
        "estado": "Pendiente",
        "fecha_creacion": "2025-07-31T00:00:00"
      },
      {
        "id_factura": 102,
        "monto": 4000000,
        "monto_pendiente": 4000000,
        "estado": "Pendiente",
        "fecha_creacion": "2025-07-31T00:00:00"
      }
    ]
  },
  "success": true
}
```

### 📍 Equivalencias de Campos

| Tu campo original | Campo API | Descripción |
|------------------|-----------|-------------|
| `capital_total` | `capital_total` | ✅ Suma de montos_pendientes |
| `intereses_causados` | `intereses_causados` | ✅ Intereses por mora |
| `intereses_contingentes` | `intereses_contingentes` | ✅ Intereses contingentes |
| `detalle_facturas` | `detalle_facturas` | ✅ Array de facturas pendientes |
| `id_factura` | `id_factura` | ✅ ID único de factura |
| `monto` | `monto` | ✅ Monto total de factura |
| `estado` | `estado` | ✅ Estado (Pendiente/Pagada/Cancelada) |

---

## 2. Modelos Pydantic Implementados

### ConsultaFacturasResponse
```python
{
    "mensaje": str           # Ej: "Consulta de saldos exitosa"
    "data": ConsultaSaldosData,
    "success": bool          # true/false
}
```

### ConsultaSaldosData
```python
{
    "fecha_proceso": date,           # Hoy
    "capital_total": float,          # Suma de pendientes
    "intereses_causados": float,     # Default: 0
    "intereses_contingentes": float, # Default: 0
    "detalle_facturas": List[DetalleFactura]
}
```

### DetalleFactura
```python
{
    "id_factura": int,
    "monto": float,
    "monto_pendiente": float,      # ← Campo NUEVO (útil para pagos parciales)
    "estado": "Pendiente"|"Pagada"|"Cancelada",
    "fecha_creacion": datetime
}
```

---

## 3. Endpoints y Cómo Usarlos

### GET /usuarios/{paciente_id}/consultaF
**Consulta saldos pendientes de un paciente (HU-22)**

```bash
curl -X GET "http://127.0.0.1:8000/usuarios/5/consultaF" \
  -H "accept: application/json"
```

**Response (200 OK):**
```json
{
  "mensaje": "Consulta de saldos exitosa",
  "data": {
    "fecha_proceso": "2025-11-29",
    "capital_total": 8500000,
    "intereses_causados": 0,
    "intereses_contingentes": 0,
    "detalle_facturas": [
      {
        "id_factura": 1,
        "monto": 4500000,
        "monto_pendiente": 4500000,
        "estado": "Pendiente",
        "fecha_creacion": "2025-11-29T15:30:00"
      }
    ]
  },
  "success": true
}
```

### GET /usuarios/{paciente_id}/facturas
**Lista TODAS las facturas de un paciente (sin filtro)**

```bash
curl -X GET "http://127.0.0.1:8000/usuarios/5/facturas" \
  -H "accept: application/json"
```

### POST /usuarios/{paciente_id}/facturas
**Crear una nueva factura (uso interno)**

```bash
curl -X POST "http://127.0.0.1:8000/usuarios/5/facturas" \
  -H "Content-Type: application/json" \
  -d '{
    "id_tratamiento": 10,
    "monto_total": 500000,
    "monto_pendiente": 500000,
    "estado_factura": "Pendiente"
  }'
```

---

## 4. Ejemplo Completo: Flujo de Facturación

### Paso 1: Paciente realiza un tratamiento
**POST /tratamientos/**
```json
{
  "nombre": "Endodoncia",
  "costo_total": 500000
}
```

### Paso 2: Sistema crea factura automáticamente
**POST /usuarios/5/facturas**
```json
{
  "id_tratamiento": 1,
  "monto_total": 500000
}
```
Response:
```json
{
  "id": 1,
  "id_paciente": 5,
  "id_tratamiento": 1,
  "monto_total": 500000,
  "monto_pendiente": 500000,
  "estado_factura": "Pendiente",
  "fecha_creacion": "2025-11-29T15:30:00"
}
```

### Paso 3: Paciente consulta saldos
**GET /usuarios/5/consultaF**

Response:
```json
{
  "mensaje": "Consulta de saldos exitosa",
  "data": {
    "fecha_proceso": "2025-11-29",
    "capital_total": 500000,
    "intereses_causados": 0,
    "intereses_contingentes": 0,
    "detalle_facturas": [
      {
        "id_factura": 1,
        "monto": 500000,
        "monto_pendiente": 500000,
        "estado": "Pendiente",
        "fecha_creacion": "2025-11-29T15:30:00"
      }
    ]
  },
  "success": true
}
```

### Paso 4: Paciente inicia pago (HU-21)
**POST /IPago/datosP**
```json
{
  "id_factura": 1,
  "monto_pagado": 500000,
  "datos_tarjeta": "4532123456789010",
  "pin_seguridad": "123"
}
```

### Paso 5: Banco confirma transacción (HU-24)
**POST /ValidacionP**
```json
{
  "estado": "Pagado",
  "id_transaccion": "TXN-2025-001"
}
```

### Paso 6: Sistema actualiza estado (HU-26)
**PUT /paciente/5/cambioEP**
```json
{
  "id_pago": 1,
  "estado_final": "Pagado",
  "id_transaccion_banco": "TXN-2025-001"
}
```

### Paso 7: Paciente consulta saldos nuevamente
**GET /usuarios/5/consultaF**

Response:
```json
{
  "mensaje": "No hay facturas pendientes",
  "data": {
    "fecha_proceso": "2025-11-29",
    "capital_total": 0,
    "intereses_causados": 0,
    "intereses_contingentes": 0,
    "detalle_facturas": []
  },
  "success": true
}
```

---

## 5. Capas Implementadas

### API Layer (`app/api/factura_api.py`)
- Endpoints REST con validación Pydantic
- Documentación automática Swagger
- Manejo de errores HTTP

### Service Layer (`app/services/factura_service.py`)
- Lógica de negocio
- Validaciones
- Orquestación de repositorios
- Transformación de datos

### Repository Layer (`app/repository/factura_repository.py`)
- CRUD completo
- Consultas especializadas
- Cálculos de saldos

### Model Layer (`app/models/factura_db.py`)
- Tabla SQLAlchemy
- Relaciones con pacientes y tratamientos

### Domain Layer (`app/domain/factura_model.py`)
- Modelos Pydantic para validación
- Serialización JSON

---

## 6. Funcionalidades Implementadas

### ✅ CRUD Básico
- `get_all_facturas()` - Todas las facturas
- `get_factura_by_id()` - Factura específica
- `create_factura()` - Crear nueva
- `update_factura()` - Actualizar
- `delete_factura()` - Eliminar

### ✅ Consultas Especializadas
- `get_facturas_by_paciente()` - Todas del paciente
- `get_facturas_pendientes_by_paciente()` - Solo pendientes (HU-22)
- `get_facturas_by_estado()` - Filtrar por estado
- `get_facturas_by_tratamiento()` - Por tratamiento

### ✅ Operaciones de Pago (HU-26)
- `marcar_como_pagada()` - Factura pagada
- `marcar_como_cancelada()` - Factura cancelada
- `actualizar_saldo_pendiente()` - Pago parcial

### ✅ Cálculos y Análisis
- `get_saldo_pendiente_paciente()` - Total pendiente
- `get_monto_pagado_paciente()` - Total pagado
- `get_resumen_paciente()` - Resumen financiero

---

## 7. Validaciones Implementadas

| Validación | Dónde | Cuando |
|-----------|-------|--------|
| Paciente existe | Service | Siempre |
| Factura existe | Service | HU-21 (inicio pago) |
| Factura pendiente | Service | HU-21, HU-26 |
| Monto > 0 | Repository | Crear/actualizar |
| Monto pago ≤ pendiente | Repository | Pago parcial |
| Saldo = 0 → Pagada | Repository | Pago completo |

---

## 8. Errores y Manejo

### 404 Not Found
```json
{
  "detail": "Paciente con ID 999 no encontrado."
}
```

### 400 Bad Request
```json
{
  "detail": "El monto pagado (600000) no puede ser mayor al pendiente (500000)"
}
```

### 500 Internal Server Error
```json
{
  "detail": "No se pudo actualizar factura 1"
}
```

---

## 9. Testing en Swagger UI

1. Accede a http://127.0.0.1:8000/docs
2. Expande "Facturas (HU-22)"
3. Prueba cada endpoint:
   - GET /usuarios/{id}/consultaF
   - GET /usuarios/{id}/facturas
   - POST /usuarios/{id}/facturas
4. Observa respuestas en tiempo real

---

## 10. Base de Datos (SQLite)

### Tabla: facturas

| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INTEGER PK | ID único |
| id_paciente | INTEGER FK | Referencia pacientes |
| id_tratamiento | INTEGER FK | Referencia tratamientos |
| monto_total | FLOAT | Monto facturado |
| monto_pendiente | FLOAT | Saldo adeudado |
| estado_factura | ENUM | Pendiente/Pagada/Cancelada |
| fecha_creacion | DATETIME | Fecha de creación |

Se crea automáticamente en startup si no existe.

---

## 11. Próximos Pasos

- [ ] Implementar PagoService para procesar pagos
- [ ] Agregar autenticación JWT
- [ ] Implementar notificaciones por email
- [ ] Crear tests unitarios
- [ ] Agregar paginación en consultas
- [ ] Implementar reportes de saldos
- [ ] Auditoría de cambios de estado
- [ ] Integración real con banco

---

**Última actualización:** 29 de Noviembre de 2025  
**Versión:** 1.0.0
