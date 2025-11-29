# 📱 Guía de Integración - Sistema de Pagos Odontología

## 1. Introducción

Este documento describe cómo integrar **el banco o procesador de pagos externo** con nuestro sistema de pagos en FastAPI.

La arquitectura soporta tanto **JSON (REST)** como **SOAP/XML (para legado)** mediante la conversión adecuada.

---

## 2. Flujo General de Pagos

```
┌─────────────────────────────────────────────────────────────────┐
│                      FLUJO DE PAGOS                             │
└─────────────────────────────────────────────────────────────────┘

Cliente (Navegador)
    │
    ├─→ POST /IPago/datosP (HU-21)
    │   └─→ Envía: número tarjeta, PIN, monto
    │
    └─ Servidor Odontología
       │
       ├─→ Valida factura pendiente
       │
       ├─→ Crea registro pago (estado: "En Proceso")
       │
       ├─→ Envía a procesador bancario
       │   (Aquí es donde se integra el BANCO)
       │
       └─ Banco procesa...
           │
           ├─→ [Asíncrono] Llama a ValidaciónP (HU-24)
           │   ├─ POST /ValidacionP
           │   └─ Envía: estado (Pagado/Rechazado), idTransaccion
           │
           └─ Servidor Odontología recibe webhook
               │
               ├─→ CambioEP (HU-26): Actualiza estado pago
               │
               └─→ NotificacionP (HU-23): Notifica cliente por email
```

---

## 3. Estructura de Datos - JSON vs SOAP/XML

### 📨 **HU-21: Inicio de Pago (IPago)**

**Request (Cliente → Sistema):**

#### JSON (FastAPI):
```json
POST /IPago/datosP HTTP/1.1
Content-Type: application/json

{
    "id_factura": 123,
    "monto_pagado": 250000.50,
    "datos_tarjeta": "4532123456789010",
    "pin_seguridad": "123"
}
```

#### XML/SOAP (Referencia legado):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:pag="http://Odontologia.com/pago">
    <soapenv:Header/>
    <soapenv:Body>
        <pag:IPago>
            <pag:idFactura>123</pag:idFactura>
            <pag:montoPagado>250000.50</pag:montoPagado>
            <pag:datosTarjeta>4532123456789010</pag:datosTarjeta>
            <pag:pinSeguridad>123</pag:pinSeguridad>
        </pag:IPago>
    </soapenv:Body>
</soapenv:Envelope>
```

**Response (Sistema → Cliente):**

#### JSON:
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 1,
    "id_factura": 123,
    "estado_pago": "En Proceso",
    "fecha_inicio": "2025-11-29T14:30:00",
    "id_transaccion_banco": null
}
```

---

### 🔔 **HU-24: Validación de Pago (ValidaciónP) - WEBHOOK**

**Este endpoint es llamado POR EL BANCO, no por el cliente.**

#### JSON (FastAPI - Recomendado):
```json
POST /ValidacionP HTTP/1.1
Content-Type: application/json

{
    "estado": "Pagado",
    "id_transaccion": "ABC123XYZ"
}
```

#### XML/SOAP (Tu estructura original - corregida):
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

**Respuesta:**

#### JSON:
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "mensaje": "Estado recibido y actualización interna (CambioEP) disparada con éxito.",
    "id_transaccion": "ABC123XYZ",
    "estado_actualizado": "Pagado"
}
```

---

### 🔄 **HU-26: Cambio de Estado (CambioEP) - API Interna**

**Este endpoint es LLAMADO INTERNAMENTE, nunca por cliente externo.**

#### JSON:
```json
PUT /paciente/5/cambioEP HTTP/1.1
Content-Type: application/json

{
    "id_pago": 1,
    "estado_final": "Pagado",
    "id_transaccion_banco": "ABC123XYZ"
}
```

**Respuesta:**
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 1,
    "id_factura": 123,
    "estado_pago": "Pagado",
    "fecha_inicio": "2025-11-29T14:30:00",
    "id_transaccion_banco": "ABC123XYZ"
}
```

---

### 📧 **HU-23: Notificación (NotificacionP) - API Interna**

**Notifica al cliente por email.**

#### JSON:
```json
POST /NotificacionP/pago HTTP/1.1
Content-Type: application/json

{
    "id": 1,
    "id_factura": 123,
    "estado_pago": "Pagado",
    "fecha_inicio": "2025-11-29T14:30:00",
    "id_transaccion_banco": "ABC123XYZ"
}
```

**Respuesta:**
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "mensaje": "Notificación en cola de envío.",
    "id_pago": 1,
    "email_cliente": "paciente@example.com",
    "asunto": "Confirmación de Pago - Pagado"
}
```

---

## 4. Integración con tu Banco/Procesador

### 4.1 Si el banco usa SOAP/XML

**Opción 1: Convertir XML a JSON en el banco (RECOMENDADO)**

Tu banco debe hacer una conversión XML → JSON antes de llamar a nuestro endpoint:

```bash
# Banco recibe respuesta XML del banco (en su sistema)
# Convierte a JSON:

{
    "estado": "Pagado",
    "id_transaccion": "ABC123XYZ"
}

# Realiza petición POST a nuestro endpoint:
curl -X POST "http://tu-servidor.com/ValidacionP" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "Pagado",
    "id_transaccion": "ABC123XYZ"
  }'
```

**Opción 2: Agregar endpoint SOAP al servidor (AVANZADO)**

Si tu banco **insiste en SOAP**, podemos agregar un endpoint que:
1. Reciba XML/SOAP
2. Convierta a JSON internamente
3. Procese igual que `/ValidacionP`

Ejemplo:
```python
from zeep import xsd
from lxml import etree

@app.post("/ValidacionP-SOAP")
def webhook_validacion_pago_soap(request: Request):
    """Recibe SOAP/XML del banco"""
    xml_body = await request.body()
    # Parsear XML → extraer Estado e idTransaccion
    # Convertir a JSON y procesar
```

---

## 5. Estados de Pago

| Estado | Descripción | Acción |
|--------|-------------|--------|
| **En Proceso** | Pago iniciado, aguardando respuesta del banco | Factura permanece "Pendiente" |
| **Pagado** | Banco confirmó, pago exitoso | Factura → "Pagada", Notificar cliente |
| **Rechazado** | Banco rechazó (fondos insuficientes, etc) | Factura permanece "Pendiente", Notificar rechazo |

---

## 6. Seguridad

### 🔒 Consideraciones Importantes

1. **NUNCA transmitir datos sensibles sin HTTPS**
   ```python
   # En producción, usar HTTPS obligatoriamente
   # En desarrollo local: http://localhost:8000 está bien
   ```

2. **Datos de tarjeta - NUNCA guardar**
   ```python
   # En la función iniciar_pago:
   # - Recibir datos_tarjeta
   # - Enviar INMEDIATAMENTE al banco
   # - NO guardar en BD
   ```

3. **Webhook ValidaciónP - Validar origen del banco**
   ```python
   # TODO: Agregar validación de firma/token
   # Asegurar que viene del banco autorizado
   
   @app.post("/ValidacionP")
   def webhook_validacion_pago(
       validacion_data: ValidacionPRequest,
       authorization: str = Header(None)
   ):
       # Validar token/firma del banco
       if not validar_firma_banco(authorization):
           raise HTTPException(status_code=403, detail="Unauthorized bank")
       # ...
   ```

4. **Rate limiting en webhook**
   ```python
   # Evitar ataques de denegación de servicio
   # Limite: 1000 requests/hora por IP del banco
   ```

---

## 7. Testing

### 7.1 Test con cURL

```bash
# 1. Iniciar pago
curl -X POST "http://127.0.0.1:8000/IPago/datosP" \
  -H "Content-Type: application/json" \
  -d '{
    "id_factura": 1,
    "monto_pagado": 100000,
    "datos_tarjeta": "4532123456789010",
    "pin_seguridad": "123"
  }'

# Respuesta esperada:
# {
#   "id": 1,
#   "id_factura": 1,
#   "estado_pago": "En Proceso",
#   "fecha_inicio": "2025-11-29T...",
#   "id_transaccion_banco": null
# }

# 2. Simular webhook del banco
curl -X POST "http://127.0.0.1:8000/ValidacionP" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "Pagado",
    "id_transaccion": "ABC123XYZ"
  }'

# Respuesta esperada:
# {
#   "mensaje": "Estado recibido y actualización interna (CambioEP) disparada con éxito.",
#   "id_transaccion": "ABC123XYZ",
#   "estado_actualizado": "Pagado"
# }
```

### 7.2 Test en Swagger UI

1. Accede a http://127.0.0.1:8000/docs
2. Expande la sección "1. Inicio de Pago (HU-21)"
3. Click en POST `/IPago/datosP`
4. Click en "Try it out"
5. Ingresa datos de prueba:
   ```json
   {
     "id_factura": 1,
     "monto_pagado": 100000,
     "datos_tarjeta": "4532123456789010",
     "pin_seguridad": "123"
   }
   ```
6. Click "Execute"

---

## 8. Errores Comunes

### ❌ Error 422: Validation Error

**Causa:** Datos inválidos en request

```json
{
  "detail": [
    {
      "loc": ["body", "monto_pagado"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

**Solución:** Validar datos antes de enviar:
- `monto_pagado` debe ser > 0
- `datos_tarjeta` debe tener 12-19 dígitos
- `pin_seguridad` debe tener 3-4 dígitos

### ❌ Error 404: Not Found

**Causa:** Ruta incorrecta

```json
{
  "detail": "Not Found"
}
```

**Solución:** Verificar rutas exactas:
- `/IPago/datosP` (NO `/ipago/datos` )
- `/ValidacionP` (NO `/validacion` )
- `/paciente/{id}/cambioEP` (NO `/cambioep` )

### ❌ Error 400: Bad Request

**Causa:** Falta un campo requerido

```json
{
  "detail": [
    {
      "loc": ["body", "estado"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Solución:** Incluir todos los campos requeridos en request

---

## 9. Variables de Entorno

Crear archivo `.env` en raíz del proyecto:

```bash
# .env

# Base de datos
DATABASE_URL=sqlite:///./odontologia_db.db

# API
API_TITLE=Web Service de Pagos Odontología
API_VERSION=1.0.0
DEBUG=true

# Banco (si aplica)
BANK_API_URL=https://api.banco.com/pagos
BANK_API_KEY=tu-clave-api-segura
BANK_WEBHOOK_SECRET=tu-secreto-webhook

# Email (para notificaciones)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=notificaciones@odontologia.com
SMTP_PASSWORD=tu-contraseña-app
```

---

## 10. Próximos Pasos

- [ ] Implementar `PagoService` con validaciones completas
- [ ] Implementar `CambioEstadoService` para actualizar estado
- [ ] Implementar integración real con procesador bancario
- [ ] Agregar validación de firma en webhook ValidaciónP
- [ ] Implementar reintento automático en casos de fallo
- [ ] Agregar logging de todas las transacciones
- [ ] Crear tests automatizados para flujo completo
- [ ] Documentar endpoints en Swagger (✅ Ya hecho)

---

## 📞 Contacto

Para preguntas de integración, contactar a:
- **Equipo Desarrollo:** dev@odontologia.com
- **Documentación:** docs.odontologia.com

---

**Última actualización:** 29 de Noviembre de 2025  
**Versión:** 1.0.0
