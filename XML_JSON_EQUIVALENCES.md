# 🔄 Equivalencias XML/SOAP ↔ JSON

Este archivo muestra las **equivalencias exactas** entre las estructuras SOAP/XML que proporcionaste y los modelos JSON que usa FastAPI.

---

## 📋 Tabla Resumen

| Componente | XML/SOAP | JSON | Endpoint |
|-----------|----------|------|----------|
| **Inicio Pago** | IPago | PagoRequest | POST /IPago/datosP |
| **Validación** | ValidaciónP | ValidacionPRequest | POST /ValidacionP |
| **Cambio Estado** | CambioEP | CambioEPRequest | PUT /paciente/{id}/cambioEP |

---

## 1. IPago - Inicio de Pago (HU-21)

### ✅ JSON (FastAPI - RECOMENDADO)

```json
{
  "id_factura": 123,
  "monto_pagado": 250000.50,
  "datos_tarjeta": "4532123456789010",
  "pin_seguridad": "123"
}
```

**cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/IPago/datosP" \
  -H "Content-Type: application/json" \
  -d '{
    "id_factura": 123,
    "monto_pagado": 250000.50,
    "datos_tarjeta": "4532123456789010",
    "pin_seguridad": "123"
  }'
```

### 📦 XML/SOAP (Referencia)

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

### 📤 Respuesta JSON

```json
{
  "id": 1,
  "id_factura": 123,
  "estado_pago": "En Proceso",
  "fecha_inicio": "2025-11-29T14:30:00",
  "id_transaccion_banco": null
}
```

### 📤 Respuesta XML/SOAP (Equivalente)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:pag="http://Odontologia.com/pago">
    <soapenv:Header/>
    <soapenv:Body>
        <pag:IPagoResponse>
            <pag:id>1</pag:id>
            <pag:idFactura>123</pag:idFactura>
            <pag:estadoPago>En Proceso</pag:estadoPago>
            <pag:fechaInicio>2025-11-29T14:30:00</pag:fechaInicio>
            <pag:idTransaccionBanco/>
        </pag:IPagoResponse>
    </soapenv:Body>
</soapenv:Envelope>
```

---

## 2. ValidaciónP - Validación del Banco (HU-24)

### ✅ JSON (FastAPI - RECOMENDADO)

**Request (Banco → Sistema):**

```json
{
  "estado": "Pagado",
  "id_transaccion": "ABC123XYZ"
}
```

**cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/ValidacionP" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "Pagado",
    "id_transaccion": "ABC123XYZ"
  }'
```

### 📦 XML/SOAP (Tu estructura original - CORREGIDA)

**Request (Banco → Sistema):**

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

### 📤 Respuesta JSON

```json
{
  "mensaje": "Estado recibido y actualización interna (CambioEP) disparada con éxito.",
  "id_transaccion": "ABC123XYZ",
  "estado_actualizado": "Pagado"
}
```

### 📤 Respuesta XML/SOAP (Equivalente)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:pag="http://Odontologia.com/pago">
    <soapenv:Header/>
    <soapenv:Body>
        <pag:ValidaciónPResponse>
            <pag:mensaje>Estado recibido y actualización interna (CambioEP) disparada con éxito.</pag:mensaje>
            <pag:idTransaccion>ABC123XYZ</pag:idTransaccion>
            <pag:estadoActualizado>Pagado</pag:estadoActualizado>
        </pag:ValidaciónPResponse>
    </soapenv:Body>
</soapenv:Envelope>
```

---

## 3. CambioEP - Cambio de Estado (HU-26)

### ✅ JSON (FastAPI - RECOMENDADO)

**Request (Sistema interno → Sistema):**

```json
{
  "id_pago": 1,
  "estado_final": "Pagado",
  "id_transaccion_banco": "ABC123XYZ"
}
```

**cURL:**
```bash
curl -X PUT "http://127.0.0.1:8000/paciente/5/cambioEP" \
  -H "Content-Type: application/json" \
  -d '{
    "id_pago": 1,
    "estado_final": "Pagado",
    "id_transaccion_banco": "ABC123XYZ"
  }'
```

### 📦 XML/SOAP (Referencia)

**Request (Sistema interno → Sistema):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:pag="http://Odontologia.com/pago">
    <soapenv:Header/>
    <soapenv:Body>
        <pag:CambioEP>
            <pag:idPago>1</pag:idPago>
            <pag:estadoFinal>Pagado</pag:estadoFinal>
            <pag:idTransaccionBanco>ABC123XYZ</pag:idTransaccionBanco>
        </pag:CambioEP>
    </soapenv:Body>
</soapenv:Envelope>
```

### 📤 Respuesta JSON

```json
{
  "id": 1,
  "id_factura": 123,
  "estado_pago": "Pagado",
  "fecha_inicio": "2025-11-29T14:30:00",
  "id_transaccion_banco": "ABC123XYZ"
}
```

### 📤 Respuesta XML/SOAP (Equivalente)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:pag="http://Odontologia.com/pago">
    <soapenv:Header/>
    <soapenv:Body>
        <pag:CambioEPResponse>
            <pag:id>1</pag:id>
            <pag:idFactura>123</pag:idFactura>
            <pag:estadoPago>Pagado</pag:estadoPago>
            <pag:fechaInicio>2025-11-29T14:30:00</pag:fechaInicio>
            <pag:idTransaccionBanco>ABC123XYZ</pag:idTransaccionBanco>
        </pag:CambioEPResponse>
    </soapenv:Body>
</soapenv:Envelope>
```

---

## 4. NotificacionP - Notificación al Cliente (HU-23)

### ✅ JSON (FastAPI)

**Request (Sistema interno → Sistema):**

```json
{
  "id": 1,
  "id_factura": 123,
  "estado_pago": "Pagado",
  "fecha_inicio": "2025-11-29T14:30:00",
  "id_transaccion_banco": "ABC123XYZ"
}
```

**cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/NotificacionP/pago" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "id_factura": 123,
    "estado_pago": "Pagado",
    "fecha_inicio": "2025-11-29T14:30:00",
    "id_transaccion_banco": "ABC123XYZ"
  }'
```

### 📤 Respuesta JSON

```json
{
  "mensaje": "Notificación en cola de envío.",
  "id_pago": 1,
  "email_cliente": "paciente@example.com",
  "asunto": "Confirmación de Pago - Pagado"
}
```

---

## 5. Conversión XML → JSON

Si tu banco envía **SOAP/XML**, aquí está cómo convertir:

### Paso 1: Recibir SOAP del banco

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

### Paso 2: Extraer datos

| Campo SOAP | Campo JSON |
|-----------|-----------|
| `pag:Estado` | `estado` |
| `pag:idTransaccion` | `id_transaccion` |

### Paso 3: Convertir a JSON

```json
{
  "estado": "Pagado",
  "id_transaccion": "ABC123XYZ"
}
```

### Paso 4: Enviar a FastAPI

```bash
curl -X POST "http://127.0.0.1:8000/ValidacionP" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "Pagado",
    "id_transaccion": "ABC123XYZ"
  }'
```

---

## 6. Errores Comunes en Conversión

### ❌ Error 1: Nombres en snake_case vs camelCase

```json
// ❌ INCORRECTO
{
  "estado_pago": "Pagado",          // Debe ser "estado"
  "idTransaccion": "ABC123XYZ"      // Debe ser "id_transaccion"
}

// ✅ CORRECTO
{
  "estado": "Pagado",
  "id_transaccion": "ABC123XYZ"
}
```

### ❌ Error 2: Tipos de datos

```json
// ❌ INCORRECTO
{
  "estado": "Pagado",
  "id_transaccion": 123             // String, no número
}

// ✅ CORRECTO
{
  "estado": "Pagado",
  "id_transaccion": "ABC123XYZ"     // String
}
```

### ❌ Error 3: Estados inválidos

```json
// ❌ INCORRECTO
{
  "estado": "pagado"                // Minúscula
  // o
  "estado": "PAGADO"                // Mayúscula
}

// ✅ CORRECTO
{
  "estado": "Pagado"                // Exactamente así
}
```

Estados válidos: `"En Proceso"`, `"Pagado"`, `"Rechazado"`

---

## 7. Script Python para Conversión

Si necesitas convertir XML → JSON automáticamente:

```python
import xml.etree.ElementTree as ET
import json

def xml_a_json_validacion(xml_string):
    """Convierte XML de ValidaciónP a JSON"""
    root = ET.fromstring(xml_string)
    
    # Namespace
    ns = {'pag': 'http://Odontologia.com/pago'}
    
    # Extraer datos
    validacion = root.find('.//pag:ValidaciónP', ns)
    estado = validacion.find('pag:Estado', ns).text
    id_transaccion = validacion.find('pag:idTransaccion', ns).text
    
    # Convertir a JSON
    resultado = {
        "estado": estado,
        "id_transaccion": id_transaccion
    }
    
    return json.dumps(resultado)

# Ejemplo
xml_banco = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:pag="http://Odontologia.com/pago">
    <soapenv:Header/>
    <soapenv:Body>
        <pag:ValidaciónP>
            <pag:Estado>Pagado</pag:Estado>
            <pag:idTransaccion>ABC123XYZ</pag:idTransaccion>
        </pag:ValidaciónP>
    </soapenv:Body>
</soapenv:Envelope>"""

json_resultado = xml_a_json_validacion(xml_banco)
print(json_resultado)
# Output: {"estado": "Pagado", "id_transaccion": "ABC123XYZ"}
```

---

## 8. Resumen

✅ **Usa JSON** - Es lo soportado nativamente por FastAPI  
✅ **Convierte XML a JSON** - Si tu banco usa SOAP  
✅ **Valida tipos de datos** - String, número, booleano, etc.  
✅ **Usa nombres exactos** - `estado`, `id_transaccion`, etc.  
✅ **Usa estados correctos** - "En Proceso", "Pagado", "Rechazado"  

---

**Última actualización:** 29 de Noviembre de 2025  
**Versión:** 1.0.0
