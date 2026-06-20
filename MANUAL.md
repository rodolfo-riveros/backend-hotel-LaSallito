# Manual de Usuario — Sistema PMS Hotelero IES La Salle

## 1. Introducción

Sistema de gestión hotelera (PMS) con módulos de reservas, check-in/check-out, facturación electrónica simulada, housekeeping e inventario.

---

## 2. Primeros pasos

### 2.1 Ingreso al sistema

**Endpoint:** `POST /api/v1/auth/login`

Enviar:
```json
{
  "email": "usuario@correo.com",
  "password": "******"
}
```

Recibes:
```json
{
  "access_token": "eyJhbGciOi...",
  "user": {
    "id": "uuid",
    "nombre_completo": "Juan Pérez",
    "rol": "recepcionista",
    "hotel_id": "uuid",
    "activo": true
  }
}
```

El `access_token` debe enviarse en **cada** request como:
```
Authorization: Bearer eyJhbGciOi...
```

Si las credenciales son incorrectas, obtienes error **401 Unauthorized**.

### 2.2 Roles del sistema

| Rol | Acceso |
|-----|--------|
| `administrador` | Todo el sistema |
| `supervisor` | Configuración limitada, reportes |
| `recepcionista` | Check-in/out, reservas, cobros |
| `auditor_nocturno` | Solo auditoría y cierres |
| `ama_llaves` | Solo housekeeping |

---

## 3. Dashboard — Pantalla principal

Al ingresar, el dashboard muestra un resumen del día:

```
POST /api/v1/dashboard/hoy

Respuesta:
- Habitaciones: total, libres, ocupadas, en limpieza, mantenimiento
- % Ocupación
- Llegadas hoy / Salidas hoy
- Ingresos del día
```

### Rack de habitaciones

```
GET /api/v1/dashboard/rack-habitaciones

Vista general de cada habitación:
- Número, piso, tipo
- Estado: libre, ocupada, limpieza, mantenimiento, bloqueada
- Huésped actual (si aplica)
```

### Huéspedes in-house

```
GET /api/v1/dashboard/huespedes-in-house

Lista de huéspedes actualmente hospedados.
```

### Reportes

- `GET /api/v1/dashboard/reporte-ocupacion` — Ocupación diaria
- `GET /api/v1/dashboard/reporte-ingresos` — Ingresos por categoría

---

## 4. Gestión de Hoteles (solo admin)

### Configurar hotel

```
POST /api/v1/hoteles
PUT  /api/v1/hoteles/{id}
```

Campos: nombre, dirección, RUC, teléfono, logo, horarios check-in/out, % IGV, % servicio.

### Tipos de habitación

```
GET/POST /api/v1/hoteles/{hotel_id}/tipos-habitacion
PUT /api/v1/hoteles/{hotel_id}/tipos-habitacion/{id}
```

Se define: nombre, capacidad máxima, descripción, amenidades (WiFi, TV, etc.).

### Habitaciones

```
GET /api/v1/hoteles/{hotel_id}/habitaciones?estado=libre
POST /api/v1/hoteles/{hotel_id}/habitaciones
PUT /api/v1/hoteles/{hotel_id}/habitaciones/{id}
```

Cada habitación tiene: número, piso, tipo, estado (libre/ocupada/limpieza/mantenimiento/bloqueada).

### Temporadas

```
GET/POST /api/v1/hoteles/{hotel_id}/temporadas
```

Define rangos de fecha (ej: "Temporada Alta: 01-Dic al 28-Feb").

### Tarifas

```
GET /api/v1/hoteles/{hotel_id}/tarifas?tipo_habitacion_id=uuid
POST /api/v1/hoteles/{hotel_id}/tarifas
PUT /api/v1/hoteles/{hotel_id}/tarifas/{id}
```

Precio por noche según tipo de habitación y temporada.

### Políticas de cancelación

```
GET/POST /api/v1/hoteles/{hotel_id}/politicas-cancelacion
```

Define penalidad por cancelación en porcentaje.

---

## 5. Huéspedes

### Registrar huésped

```json
POST /api/v1/huespedes

{
  "nombres": "Juan",
  "apellidos": "Pérez García",
  "tipo_documento": "DNI",
  "numero_documento": "12345678",
  "nacionalidad": "Peruana",
  "email": "juan@correo.com",
  "telefono": "999888777",
  "es_vip": false
}
```

### Buscar huésped

```
GET /api/v1/huespedes/?search=Juan
GET /api/v1/huespedes/buscar/documento?tipo_documento=DNI&numero_documento=12345678
```

La búsqueda general busca en nombres, apellidos, documento y email.

---

## 6. Reservas

### Crear reserva

```json
POST /api/v1/reservas

{
  "hotel_id": "uuid",
  "huesped_id": "uuid",
  "tipo_habitacion_id": "uuid",
  "fecha_llegada": "2025-07-01",
  "fecha_salida": "2025-07-03",
  "numero_huespedes": 2,
  "canal": "presencial",
  "estado": "pendiente"
}
```

Canales disponibles: `presencial`, `booking`, `expedia`, `directo`, `whatsapp`, `otros`.

Estados: `pendiente`, `confirmada`, `cancelada`, `no_show`.

### Agregar huéspedes adicionales a una reserva

```json
POST /api/v1/reservas/{id}/huespedes-adicionales
{
  "reserva_id": "uuid",
  "huesped_id": "uuid"
}
```

### Cancelar reserva

```
POST /api/v1/reservas/{id}/cancelar?motivo=Cliente no confirmó
```

---

## 7. Check-in / Estadías

### Listar estadías activas

```
GET /api/v1/estadias/?activas=true
```

### Realizar check-in

```json
POST /api/v1/estadias/checkin

{
  "hotel_id": "uuid",
  "reserva_id": "uuid",
  "habitacion_id": "uuid",
  "huesped_id": "uuid",
  "deposito_garantia": 0.00
}
```

El sistema crea automáticamente:
- La estadía con fecha de check-in real
- Un **folio** asociado (cuenta del huésped)
- La habitación cambia a estado "ocupada"

### Verificar documentos en check-in

```json
POST /api/v1/estadias/documentos-verificados

{
  "estadia_id": "uuid",
  "huesped_id": "uuid",
  "tipo_documento": "DNI",
  "numero_documento": "12345678"
}
```

### Realizar check-out

```
POST /api/v1/estadias/{id}/checkout
```

Cierra el folio y la estadía.

### Calificar estadía

```
PUT /api/v1/estadias/{id}/calificar?calificacion=4
```

Calificación de 1 a 5.

---

## 8. Facturación (Folios y Cargos)

### El folio

Cada estadía tiene un **folio** (cuenta). El folio acumula todos los cargos y pagos del huésped.

```
GET /api/v1/folios/?abiertos=true
GET /api/v1/folios/{id}
```

Respuesta:
```json
{
  "id": "uuid",
  "hotel_id": "uuid",
  "estadia_id": "uuid",
  "saldo": 250.00,
  "abierto": true
}
```

### Conceptos de cargo (catálogo)

Administrador o supervisor configura los conceptos facturables:

```
GET  /api/v1/folios/conceptos-cargo
POST /api/v1/folios/conceptos-cargo
```

Ejemplos: "Alojamiento", "Restaurant", "Lavandería", "Minibar", "Consumo bar".

### Agregar cargos al folio

```json
POST /api/v1/folios/{folio_id}/movimientos

{
  "tipo": "cargo",
  "concepto_id": "uuid",
  "descripcion": "Cena restaurant",
  "cantidad": 2,
  "precio_unitario": 45.00,
  "monto_total": 90.00
}
```

Tipos de movimiento:
- `cargo` — consumo o servicio (aumenta saldo)
- `abono` — descuento o ajuste (disminuye saldo)
- `pago` — pago recibido (disminuye saldo, requiere `metodo_pago`)

Métodos de pago: `efectivo`, `tarjeta`, `transferencia`, `yape`, `plin`.

### Anular un movimiento

```json
PUT /api/v1/folios/movimientos/{id}/anular

{
  "motivo_anulacion": "Cargo incorrecto"
}
```

### Ver movimientos del folio

```
GET /api/v1/folios/{folio_id}/movimientos
```

Muestra el detalle completo incluyendo montos base, IGV, servicio, total y si está anulado.

---

## 9. Emitir comprobante (Simulador SUNAT)

### Emitir boleta o factura

```json
POST /api/v1/folios/{folio_id}/comprobantes

{
  "tipo": "boleta",
  "razon_social_cliente": "Juan Pérez",
  "ruc_dni_cliente": "12345678",
  "direccion_cliente": "Av. Siempre Viva 123"
}
```

El sistema **calcula automáticamente**:
- **Serie**: B001 (boletas) / F001 (facturas)
- **Correlativo**: autoincremental por serie y hotel
- **Subtotal**, **IGV (18%)**, **Servicio**
- **Total** basado en los movimientos del folio
- **Hash SUNAT** simulado (SHA-256)

Respuesta:
```json
{
  "serie": "B001",
  "correlativo": 5,
  "subtotal": 254.24,
  "igv": 45.76,
  "servicio": 0.00,
  "total": 300.00,
  "sunat_hash": "A1B2C3D4...",
  "estado": "emitido"
}
```

### Consultar comprobante

```
GET /api/v1/folios/comprobantes/{id}
```

**Importante:** Si el saldo del folio es 0 o negativo, el sistema rechaza la emisión con error "No hay cargos pendientes por facturar".

---

## 10. Housekeeping (Ama de llaves)

### Tareas de limpieza

```
GET  /api/v1/housekeeping/tareas-limpieza?fecha=2025-06-19&estado=pendiente
POST /api/v1/housekeeping/tareas-limpieza
PUT  /api/v1/housekeeping/tareas-limpieza/{id}
```

Estados: `pendiente`, `en_proceso`, `completada`, `inspeccionada`.

Prioridades: `baja`, `normal`, `alta`.

```json
POST /api/v1/housekeeping/tareas-limpieza

{
  "hotel_id": "uuid",
  "habitacion_id": "uuid",
  "fecha": "2025-06-19",
  "prioridad": "normal",
  "notas": "Cambiar sábanas y toallas"
}
```

### Asignar tarea

```
POST /api/v1/housekeeping/tareas-limpieza/{id}/asignar?usuario_id=uuid
```

Cambia estado a `en_proceso` y asigna el personal.

### Plan de limpieza del día

```
GET /api/v1/dashboard/plan-limpieza-hoy
```

Vista rápida con prioridad, estado y asignado.

### Objetos perdidos

```
GET  /api/v1/housekeeping/objetos-perdidos?entregado=false
POST /api/v1/housekeeping/objetos-perdidos
PUT  /api/v1/housekeeping/objetos-perdidos/{id}
```

```json
POST /api/v1/housekeeping/objetos-perdidos

{
  "habitacion_id": "uuid",
  "descripcion": "Reloj plateado marca Casio",
  "ubicacion": "Habitación 203",
  "notas": "Dejar en recepción"
}
```

---

## 11. Inventario (supervisor/admin)

### Productos

```
GET  /api/v1/inventario/productos?stock_bajo=true&categoria=...
POST /api/v1/inventario/productos
PUT  /api/v1/inventario/productos/{id}
```

```json
POST /api/v1/inventario/productos

{
  "codigo": "PROD-001",
  "nombre": "Jabón líquido 500ml",
  "categoria": "Aseo",
  "unidad_medida": "unidad",
  "precio_compra": 8.50,
  "precio_venta": 15.00,
  "stock_actual": 20,
  "stock_minimo": 5
}
```

### Movimientos de inventario

```
GET  /api/v1/inventario/movimientos?producto_id=uuid
POST /api/v1/inventario/movimientos
```

```json
POST /api/v1/inventario/movimientos

{
  "producto_id": "uuid",
  "tipo": "entrada",
  "cantidad": 10,
  "motivo": "Compra proveedor"
}
```

Tipos: `entrada`, `salida`, `ajuste`.

---

## 12. Auditoría y Cierre Nocturno

### Log de auditoría

```
GET /api/v1/auditoria/?tabla_afectada=reservas&accion=INSERT&limit=100
```

Solo accesible para `administrador` y `auditor_nocturno`.

### Cierre nocturno

```json
POST /api/v1/auditoria/cierres-nocturnos

{
  "hotel_id": "uuid",
  "fecha": "2025-06-19",
  "observaciones": "Todo en orden"
}
```

Genera un reporte con:
- Total ingresos, alojamiento, alimentos, servicios, otros
- Habitaciones ocupadas / disponibles
- Porcentaje de ocupación

---

## 13. Gestión de Usuarios (admin)

### Crear usuario

```json
POST /api/v1/auth/register

{
  "email": "nuevo@correo.com",
  "password": "123456",
  "nombre_completo": "María López",
  "rol": "recepcionista",
  "hotel_id": "uuid"
}
```

### Listar y editar usuarios

```
GET  /api/v1/auth/perfiles
GET  /api/v1/auth/perfiles/{id}
PUT  /api/v1/auth/perfiles/{id}
```

### Ver perfil actual

```
GET /api/v1/auth/me
```

---

## 14. Resolución de problemas comunes

| Problema | Causa | Solución |
|----------|-------|----------|
| Error 401 login | Credenciales incorrectas | Verificar email y contraseña |
| Perfil no encontrado | Usuario en Auth pero no en tabla `perfiles` | Insertar registro en `perfiles` manualmente |
| Error 403 | Rol no autorizado para la acción | Verificar que el usuario tenga el rol correcto |
| No hay cargos por facturar | Saldo del folio es 0 o negativo | Agregar movimientos tipo "cargo" al folio |
| Habitación no disponible | Estado no es "libre" o está ocupada | Verificar rack de habitaciones |

---

## 15. Glosario

| Término | Significado |
|---------|-------------|
| Folio | Cuenta o factura abierta del huésped durante su estadía |
| Check-in | Registro de ingreso del huésped al hotel |
| Check-out | Registro de salida y cierre de cuenta |
| Rack | Tablero visual del estado de todas las habitaciones |
| In-house | Huésped actualmente alojado |
| SUNAT | Entidad tributaria peruana (simulada) |
| Serie | Prefijo del comprobante (B001=boleta, F001=factura) |
| Correlativo | Número secuencial del comprobante |
