# 📚 Documentación API - Nuevas Funcionalidades

## 🎯 Resumen de Cambios

Esta documentación describe las nuevas funcionalidades implementadas en el backend:

1. **Gestión de Horarios Fijos (Schedules)** - CRUD completo con alias `/api/schedules`
2. **Gestión de Asistencias** - CRUD completo con validaciones
3. **Validación de Ajuste de Horas** - Rango (-24 a 24)
4. **Filtrado y Consultas** - Múltiples parámetros de filtrado

---

## 🔐 Autenticación

Todos los endpoints requieren autenticación mediante token JWT en el header:

```
Authorization: Bearer {token}
```

El token se obtiene al registrarse o hacer login.

---

## 📅 HORARIOS FIJOS (SCHEDULES)

Los endpoints de horarios están disponibles tanto en `/api/horarios/` como en `/api/schedules/` (alias).

### 1. Listar Horarios del Usuario

**Endpoint:** `GET /api/schedules/`  
**Alias:** `GET /api/horarios/`  
**Autenticación:** Requerida (Monitor)

**Respuesta Exitosa (200):**
```json
[
  {
    "id": 1,
    "usuario": {
      "id": 2,
      "username": "monitor01",
      "nombre": "Juan Pérez",
      "tipo_usuario": "MONITOR",
      "tipo_usuario_display": "Monitor"
    },
    "dia_semana": 0,
    "dia_semana_display": "Lunes",
    "jornada": "M",
    "jornada_display": "Mañana",
    "sede": "SA",
    "sede_display": "San Antonio"
  }
]
```

**Valores Válidos:**
- `dia_semana`: 0-6 (0=Lunes, 1=Martes, 2=Miércoles, 3=Jueves, 4=Viernes, 5=Sábado, 6=Domingo)
- `jornada`: "M" (Mañana) o "T" (Tarde)
- `sede`: "SA" (San Antonio) o "BA" (Barcelona)

---

### 2. Crear Horario Individual

**Endpoint:** `POST /api/schedules/`  
**Alias:** `POST /api/horarios/`  
**Autenticación:** Requerida (Monitor)

**Body:**
```json
{
  "dia_semana": 0,
  "jornada": "M",
  "sede": "SA"
}
```

**Respuesta Exitosa (201):**
```json
{
  "id": 1,
  "dia_semana": 0,
  "jornada": "M",
  "sede": "SA"
}
```

**Validaciones:**
- No puede existir otro horario con la misma combinación de usuario + día + jornada

---

### 3. Crear Múltiples Horarios

**Endpoint:** `POST /api/schedules/multiple/`  
**Alias:** `POST /api/horarios/multiple/`  
**Autenticación:** Requerida (Monitor)

**Body:**
```json
{
  "horarios": [
    {
      "dia_semana": 0,
      "jornada": "M",
      "sede": "SA"
    },
    {
      "dia_semana": 1,
      "jornada": "T",
      "sede": "BA"
    },
    {
      "dia_semana": 2,
      "jornada": "M",
      "sede": "SA"
    }
  ]
}
```

**Respuesta Exitosa (201):**
```json
{
  "mensaje": "Se crearon 3 horarios exitosamente para monitor01",
  "horarios_creados": [
    {
      "id": 1,
      "usuario": {...},
      "dia_semana": 0,
      "dia_semana_display": "Lunes",
      "jornada": "M",
      "jornada_display": "Mañana",
      "sede": "SA",
      "sede_display": "San Antonio"
    },
    // ... más horarios
  ],
  "total_solicitados": 3,
  "total_creados": 3,
  "usuario": {
    "id": 2,
    "username": "monitor01",
    "nombre": "Juan Pérez"
  }
}
```

**Respuesta con Errores Parciales (207):**
```json
{
  "mensaje": "Se crearon 2 horarios exitosamente para monitor01, 1 con errores",
  "horarios_creados": [...],
  "total_solicitados": 3,
  "total_creados": 2,
  "errores": [
    "Horario 2: Ya existe un horario para Martes Mañana"
  ],
  "usuario": {...}
}
```

**Límites:**
- Mínimo: 1 horario
- Máximo: 50 horarios por petición

---

### 4. Editar Múltiples Horarios (Reemplazar Todos)

**Endpoint:** `PUT /api/schedules/edit-multiple/` o `POST /api/schedules/edit-multiple/`  
**Alias:** `PUT /api/horarios/edit-multiple/`  
**Autenticación:** Requerida (Monitor)

**Comportamiento:** Elimina TODOS los horarios existentes del usuario y crea los nuevos.

**Body:**
```json
{
  "horarios": [
    {
      "dia_semana": 3,
      "jornada": "M",
      "sede": "BA"
    },
    {
      "dia_semana": 4,
      "jornada": "T",
      "sede": "SA"
    }
  ]
}
```

**Respuesta Exitosa (200):**
```json
{
  "mensaje": "Se editaron los horarios exitosamente para monitor01",
  "horarios_eliminados": 3,
  "horarios_creados": [...],
  "total_solicitados": 2,
  "total_creados": 2,
  "usuario": {...}
}
```

---

### 5. Obtener Horario Específico

**Endpoint:** `GET /api/schedules/{id}/`  
**Alias:** `GET /api/horarios/{id}/`  
**Autenticación:** Requerida (Monitor)

**Respuesta Exitosa (200):**
```json
{
  "id": 1,
  "usuario": {...},
  "dia_semana": 0,
  "dia_semana_display": "Lunes",
  "jornada": "M",
  "jornada_display": "Mañana",
  "sede": "SA",
  "sede_display": "San Antonio"
}
```

---

### 6. Actualizar Horario

**Endpoint:** `PUT /api/schedules/{id}/`  
**Alias:** `PUT /api/horarios/{id}/`  
**Autenticación:** Requerida (Monitor)

**Body:**
```json
{
  "dia_semana": 0,
  "jornada": "T",
  "sede": "BA"
}
```

**Respuesta Exitosa (200):** Similar a la respuesta de creación

---

### 7. Eliminar Horario

**Endpoint:** `DELETE /api/schedules/{id}/`  
**Alias:** `DELETE /api/horarios/{id}/`  
**Autenticación:** Requerida (Monitor)

**Respuesta Exitosa (204):** Sin contenido

---

### 8. [DIRECTIVO] Listar Horarios de Todos los Monitores

**Endpoint:** `GET /api/directivo/schedules/`  
**Alias:** `GET /api/directivo/horarios/`  
**Autenticación:** Requerida (Directivo)

**Query Parameters:**
- `usuario_id` (opcional): Filtrar por ID de monitor
- `dia_semana` (opcional): Filtrar por día (0-6)
- `jornada` (opcional): Filtrar por jornada (M/T)
- `sede` (opcional): Filtrar por sede (SA/BA)

**Ejemplo:**
```
GET /api/directivo/schedules/?dia_semana=0&jornada=M&sede=SA
```

**Respuesta Exitosa (200):**
```json
{
  "total_horarios": 15,
  "total_monitores": 5,
  "horarios": [
    {
      "id": 1,
      "usuario": {...},
      "dia_semana": 0,
      "dia_semana_display": "Lunes",
      "jornada": "M",
      "jornada_display": "Mañana",
      "sede": "SA",
      "sede_display": "San Antonio"
    },
    // ... más horarios
  ]
}
```

---

## ✅ ASISTENCIAS

### 1. Listar Asistencias del Usuario

**Endpoint:** `GET /api/asistencias/`  
**Autenticación:** Requerida (Monitor)

**Query Parameters:**
- `fecha_inicio` (opcional): Formato YYYY-MM-DD
- `fecha_fin` (opcional): Formato YYYY-MM-DD
- `estado` (opcional): "pendiente", "autorizado", "rechazado"
- `horario_id` (opcional): ID del horario fijo

**Ejemplo:**
```
GET /api/asistencias/?fecha_inicio=2025-01-01&fecha_fin=2025-01-31&estado=pendiente
```

**Respuesta Exitosa (200):**
```json
{
  "total_asistencias": 5,
  "total_horas": 20.5,
  "asistencias": [
    {
      "id": 1,
      "usuario": {
        "id": 2,
        "username": "monitor01",
        "nombre": "Juan Pérez",
        "tipo_usuario": "MONITOR",
        "tipo_usuario_display": "Monitor"
      },
      "horario": {
        "id": 1,
        "usuario": {...},
        "dia_semana": 0,
        "dia_semana_display": "Lunes",
        "jornada": "M",
        "jornada_display": "Mañana",
        "sede": "SA",
        "sede_display": "San Antonio"
      },
      "fecha": "2025-01-15",
      "presente": true,
      "estado_autorizacion": "pendiente",
      "estado_autorizacion_display": "Pendiente",
      "horas": 4.0,
      "created_at": "2025-01-15T08:30:00Z",
      "updated_at": "2025-01-15T08:30:00Z"
    },
    // ... más asistencias
  ]
}
```

---

### 2. Crear Asistencia

**Endpoint:** `POST /api/asistencias/`  
**Autenticación:** Requerida (Monitor)

**Body:**
```json
{
  "horario_id": 1,
  "fecha": "2025-01-15",
  "presente": true,
  "horas": 4.0
}
```

**Respuesta Exitosa (201):**
```json
{
  "id": 1,
  "usuario": {...},
  "horario": {...},
  "fecha": "2025-01-15",
  "presente": true,
  "estado_autorizacion": "pendiente",
  "estado_autorizacion_display": "Pendiente",
  "horas": 4.0,
  "created_at": "2025-01-15T08:30:00Z",
  "updated_at": "2025-01-15T08:30:00Z"
}
```

**Validaciones:**
- ✅ **Unicidad:** No puede existir otra asistencia con la misma combinación usuario + fecha + horario
- ✅ **Rango de horas:** Entre 0 y 24
- ✅ **Horario válido:** El horario debe existir y pertenecer al usuario

**Errores:**

```json
// Error de unicidad (400)
{
  "non_field_errors": [
    "Ya existe un registro de asistencia para este usuario, fecha y horario."
  ]
}

// Error de rango de horas (400)
{
  "horas": [
    "Las horas deben estar entre 0 y 24."
  ]
}

// Error de horario no pertenece al usuario (403)
{
  "detail": "El horario especificado no pertenece al usuario autenticado"
}
```

---

### 3. Obtener Asistencia Específica

**Endpoint:** `GET /api/asistencias/{id}/`  
**Autenticación:** Requerida (Monitor)

**Respuesta Exitosa (200):** Similar a la respuesta de creación

---

### 4. Actualizar Asistencia

**Endpoint:** `PUT /api/asistencias/{id}/`  
**Autenticación:** Requerida (Monitor)

**Body (todos los campos son opcionales):**
```json
{
  "presente": true,
  "horas": 5.5,
  "estado_autorizacion": "pendiente"
}
```

**Respuesta Exitosa (200):** Asistencia actualizada completa

**Nota:** El monitor puede actualizar sus propias asistencias. El campo `estado_autorizacion` normalmente solo lo actualiza un directivo, pero el monitor puede modificarlo en sus propias asistencias.

---

### 5. Eliminar Asistencia

**Endpoint:** `DELETE /api/asistencias/{id}/`  
**Autenticación:** Requerida (Monitor)

**Respuesta Exitosa (204):**
```json
{
  "detail": "Asistencia eliminada exitosamente"
}
```

---

### 6. [DIRECTIVO] Listar Todas las Asistencias

**Endpoint:** `GET /api/directivo/asistencias/`  
**Autenticación:** Requerida (Directivo)

**Query Parameters:**
- `usuario_id` (opcional): Filtrar por ID de monitor
- `fecha_inicio` (opcional): Formato YYYY-MM-DD
- `fecha_fin` (opcional): Formato YYYY-MM-DD
- `estado` (opcional): "pendiente", "autorizado", "rechazado"
- `sede` (opcional): "SA" o "BA"

**Ejemplo:**
```
GET /api/directivo/asistencias/?estado=pendiente&sede=SA
```

**Respuesta Exitosa (200):**
```json
{
  "total_asistencias": 25,
  "total_horas": 100.5,
  "monitores_distintos": 8,
  "asistencias": [...]
}
```

---

### 7. [DIRECTIVO] Autorizar/Rechazar Asistencia

**Endpoint:** `PUT /api/directivo/asistencias/{id}/autorizar/`  
**Autenticación:** Requerida (Directivo)

**Body:**
```json
{
  "estado_autorizacion": "autorizado"
}
```

**Valores válidos:**
- `"pendiente"`
- `"autorizado"`
- `"rechazado"`

**Respuesta Exitosa (200):** Asistencia con estado actualizado

**Error (400):**
```json
{
  "detail": "Estado debe ser: pendiente, autorizado o rechazado"
}
```

---

## ⏰ AJUSTES DE HORAS

### Validación de Rango

**Implementado en:** `AjusteHorasCreateSerializer`

**Validaciones:**
- ✅ Rango permitido: **-24.00 a 24.00**
- ✅ No se permite valor **0**

### Crear Ajuste de Horas

**Endpoint:** `POST /api/directivo/ajustes-horas/`  
**Autenticación:** Requerida (Directivo)

**Body:**
```json
{
  "monitor_id": 2,
  "fecha": "2025-01-15",
  "cantidad_horas": 4.5,
  "motivo": "Horas extras por evento especial"
}
```

**Respuesta Exitosa (201):**
```json
{
  "id": 1,
  "usuario": {...},
  "fecha": "2025-01-15",
  "cantidad_horas": "4.50",
  "motivo": "Horas extras por evento especial",
  "creado_por": {...},
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:00Z"
}
```

**Errores de Validación (400):**
```json
// Fuera de rango
{
  "cantidad_horas": [
    "La cantidad de horas debe estar entre -24.00 y 24.00."
  ]
}

// Valor cero
{
  "cantidad_horas": [
    "La cantidad de horas no puede ser 0."
  ]
}

// Monitor no encontrado
{
  "monitor_id": [
    "Monitor no encontrado o no es de tipo MONITOR."
  ]
}
```

---

## 🔄 Resumen de Estados

### Estados de Asistencia

| Estado | Valor | Descripción |
|--------|-------|-------------|
| Pendiente | `"pendiente"` | Asistencia registrada, esperando aprobación |
| Autorizado | `"autorizado"` | Asistencia aprobada por directivo |
| Rechazado | `"rechazado"` | Asistencia rechazada por directivo |

---

## 📊 Ejemplos de Uso Completos

### Ejemplo 1: Crear Horario Semanal Completo

```javascript
// Frontend: Crear horarios de toda la semana
const crearHorarioSemanal = async (token) => {
  const response = await fetch('http://localhost:8000/api/schedules/multiple/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      horarios: [
        { dia_semana: 0, jornada: 'M', sede: 'SA' }, // Lunes Mañana
        { dia_semana: 1, jornada: 'M', sede: 'SA' }, // Martes Mañana
        { dia_semana: 2, jornada: 'T', sede: 'BA' }, // Miércoles Tarde
        { dia_semana: 3, jornada: 'M', sede: 'SA' }, // Jueves Mañana
        { dia_semana: 4, jornada: 'T', sede: 'BA' }  // Viernes Tarde
      ]
    })
  });
  
  return await response.json();
};
```

### Ejemplo 2: Registrar Asistencia Diaria

```javascript
// Frontend: Registrar asistencia del día
const registrarAsistencia = async (token, horarioId) => {
  const fechaHoy = new Date().toISOString().split('T')[0];
  
  const response = await fetch('http://localhost:8000/api/asistencias/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      horario_id: horarioId,
      fecha: fechaHoy,
      presente: true,
      horas: 4.0
    })
  });
  
  return await response.json();
};
```

### Ejemplo 3: Consultar Asistencias del Mes

```javascript
// Frontend: Obtener asistencias del mes actual
const obtenerAsistenciasMes = async (token) => {
  const hoy = new Date();
  const primerDia = new Date(hoy.getFullYear(), hoy.getMonth(), 1)
    .toISOString().split('T')[0];
  const ultimoDia = new Date(hoy.getFullYear(), hoy.getMonth() + 1, 0)
    .toISOString().split('T')[0];
  
  const response = await fetch(
    `http://localhost:8000/api/asistencias/?fecha_inicio=${primerDia}&fecha_fin=${ultimoDia}`,
    {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );
  
  return await response.json();
};
```

### Ejemplo 4: Filtrar Horarios por Día

```javascript
// Frontend: Obtener horarios de un día específico (ej: Lunes)
const obtenerHorariosLunes = async (tokenDirectivo) => {
  const response = await fetch(
    'http://localhost:8000/api/directivo/schedules/?dia_semana=0',
    {
      headers: {
        'Authorization': `Bearer ${tokenDirectivo}`
      }
    }
  );
  
  return await response.json();
};
```

### Ejemplo 5: Aprobar Asistencia (Directivo)

```javascript
// Frontend: Directivo aprueba una asistencia
const aprobarAsistencia = async (tokenDirectivo, asistenciaId) => {
  const response = await fetch(
    `http://localhost:8000/api/directivo/asistencias/${asistenciaId}/autorizar/`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokenDirectivo}`
      },
      body: JSON.stringify({
        estado_autorizacion: 'autorizado'
      })
    }
  );
  
  return await response.json();
};
```

---

## 🧪 Testing

Se incluye un script de prueba completo en `test_api.py`.

### Ejecutar Tests

```bash
# 1. Asegúrate de que el servidor Django esté corriendo
python manage.py runserver

# 2. En otra terminal, ejecuta el script de tests
python test_api.py
```

El script prueba:
- ✅ Registro y login de monitores
- ✅ CRUD completo de horarios
- ✅ CRUD completo de asistencias
- ✅ Validación de unicidad de asistencias
- ✅ Validación de rango de horas (0-24)
- ✅ Validación de ajuste de horas (-24 a 24)
- ✅ Filtrado de horarios
- ✅ Filtrado de asistencias

---

## ⚠️ Notas Importantes

### 1. Validación de Unicidad
- Una asistencia es única por la combinación: **usuario + fecha + horario**
- Si intentas crear una asistencia duplicada, recibirás un error 400

### 2. Permisos
- **Monitores:** Pueden gestionar sus propios horarios y asistencias
- **Directivos:** Pueden ver todos los horarios y asistencias, y autorizar/rechazar

### 3. Alias de Endpoints
- Los endpoints `/api/schedules/` son **exactamente iguales** a `/api/horarios/`
- Usa el que prefieras para mantener consistencia en tu frontend

### 4. Fechas
- Todas las fechas deben estar en formato **YYYY-MM-DD**
- Ejemplo: `"2025-01-15"`

### 5. Horas
- Las horas se manejan como números decimales
- Rango válido: **0.00 a 24.00**
- Ejemplo: `4.5` (4 horas y 30 minutos)

### 6. Ajustes de Horas
- Rango válido: **-24.00 a 24.00**
- No se permite **0**
- Valores negativos restan horas, positivos agregan

---

## 📝 Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Operación exitosa |
| 201 | Created - Recurso creado exitosamente |
| 204 | No Content - Eliminación exitosa |
| 207 | Multi-Status - Éxito parcial (algunos elementos fallaron) |
| 400 | Bad Request - Error en los datos enviados |
| 401 | Unauthorized - Token inválido o no proporcionado |
| 403 | Forbidden - No tienes permisos para esta acción |
| 404 | Not Found - Recurso no encontrado |

---

## 🚀 Próximos Pasos para el Frontend

1. **Integrar endpoints de horarios (schedules)**
   - Formulario para crear/editar horarios
   - Vista de horario semanal
   - Botón para editar horario completo

2. **Integrar endpoints de asistencias**
   - Formulario para registrar asistencia diaria
   - Lista de asistencias con filtros
   - Vista de estadísticas (total horas, etc.)

3. **Vista de directivo**
   - Dashboard con horarios de todos los monitores
   - Lista de asistencias pendientes de aprobación
   - Botones para autorizar/rechazar asistencias

4. **Validaciones en el frontend**
   - Verificar rangos de horas antes de enviar
   - Mostrar errores de unicidad de forma amigable
   - Validar formatos de fecha

---

## 📞 Soporte

Para preguntas o problemas:
- Revisa esta documentación completa
- Ejecuta el script de tests para verificar funcionamiento
- Verifica los códigos de estado HTTP para identificar errores

**¡Buena suerte con la implementación del frontend!** 🎉

