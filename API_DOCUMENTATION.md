# 📚 Documentación de la API - Sistema de Monitoreo

## 🔐 Autenticación

Todos los endpoints (excepto login y registro) requieren autenticación JWT.

**Headers para endpoints protegidos:**
```
Authorization: Bearer <token>
```

---

## 🚀 Endpoints Disponibles (Laboratorio I)

### ✅ HU1: Registro de Monitor
### ✅ HU2: Login y Obtención de Token
### ✅ HU3: Gestión de Horarios
### ✅ HU7A: Ajustes Manuales de Horas
### ✅ HU9: Administración de Configuraciones del Sistema

---

## 🔐 Autenticación (HU1, HU2)

### Registro de Usuario
**POST** `/example/registro/`

**Descripción:** Crea un nuevo usuario con tipo MONITOR automáticamente. Los usuarios no pueden elegir su tipo.

**Body:**
```json
{
  "username": "nuevo_usuario",
  "nombre": "Usuario Nuevo",
  "password": "password123",
  "confirm_password": "password123"
}
```

**Validaciones:**
- `username`: Único, requerido
- `nombre`: Requerido
- `password`: Mínimo 6 caracteres, requerido
- `confirm_password`: Debe coincidir con password

**Respuesta Exitosa (201):**
```json
{
  "mensaje": "Usuario registrado exitosamente",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "usuario": {
    "id": 3,
    "username": "nuevo_usuario",
    "nombre": "Usuario Nuevo",
    "tipo_usuario": "MONITOR",
    "tipo_usuario_display": "Monitor"
  }
}
```

**Respuesta de Error (400):**
```json
{
  "username": ["Este nombre de usuario ya está en uso."]
}
```

**O:**
```json
{
  "non_field_errors": ["Las contraseñas no coinciden."]
}
```

---

### Login de Usuario
**POST** `/example/login/`

**Body:**
```json
{
  "password": "Admin#1234",
  "nombre_de_usuario": "superusuario"
}
```

**Respuesta Exitosa (200):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "usuario": {
    "id": 1,
    "username": "superusuario",
    "nombre": "superusuario",
    "tipo_usuario": "DIRECTIVO",
    "tipo_usuario_display": "Directivo"
  }
}
```

**Respuesta de Error (404):**
```json
{
  "error": "Usuario no encontrado"
}
```

**Respuesta de Error (401):**
```json
{
  "error": "Contraseña incorrecta"
}
```

---

### Obtener Usuario Actual
**GET** `/example/usuario/actual/`

**Headers:** `Authorization: Bearer <token>`

**Respuesta (200):**
```json
{
  "id": 1,
  "username": "superusuario",
  "nombre": "superusuario",
  "tipo_usuario": "DIRECTIVO",
  "tipo_usuario_display": "Directivo"
}
```

---

## 🕐 Horarios Fijos (HU3)

### Listar Horarios del Usuario
**GET** `/example/horarios/`

**Headers:** `Authorization: Bearer <token>`

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "usuario": {
      "id": 1,
      "username": "monitor1",
      "nombre": "Juan Monitor",
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

---

### Crear Horario Fijo
**POST** `/example/horarios/`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "dia_semana": 0,
  "jornada": "M",
  "sede": "SA"
}
```

**Respuesta (201):**
```json
{
  "dia_semana": 0,
  "jornada": "M",
  "sede": "SA"
}
```

---

### Obtener Horario Específico
**GET** `/example/horarios/{id}/`

**Headers:** `Authorization: Bearer <token>`

**Respuesta (200):**
```json
{
  "id": 1,
  "usuario": {
    "id": 1,
    "username": "monitor1",
    "nombre": "Juan Monitor",
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
```

---

### Actualizar Horario
**PUT** `/example/horarios/{id}/`

**Headers:** `Authorization: Bearer <token>`

**Body:**
```json
{
  "dia_semana": 1,
  "jornada": "T",
  "sede": "BA"
}
```

**Respuesta (200):**
```json
{
  "dia_semana": 1,
  "jornada": "T",
  "sede": "BA"
}
```

---

### Eliminar Horario
**DELETE** `/example/horarios/{id}/`

**Headers:** `Authorization: Bearer <token>`

**Respuesta (204):** Sin contenido

---

### Crear Múltiples Horarios
**POST** `/example/horarios/multiple/`

**Headers:** `Authorization: Bearer <token>`

**Descripción:** Crea múltiples horarios en una sola petición. No elimina los existentes.

**Body:**
```json
{
  "horarios": [
    {"dia_semana": 0, "jornada": "M", "sede": "SA"},
    {"dia_semana": 2, "jornada": "T", "sede": "BA"},
    {"dia_semana": 4, "jornada": "M", "sede": "SA"}
  ]
}
```

**Respuesta (201):**
```json
{
  "mensaje": "Se crearon 3 horarios exitosamente para monitor1",
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
    }
  ],
  "total_solicitados": 3,
  "total_creados": 3,
  "usuario": {
    "id": 1,
    "username": "monitor1",
    "nombre": "Juan Monitor"
  }
}
```

---

### Editar Múltiples Horarios (Reemplazar Todos)
**PUT** o **POST** `/example/horarios/edit-multiple/`

**Headers:** `Authorization: Bearer <token>`

**Descripción:** Elimina TODOS los horarios existentes del usuario y crea los nuevos especificados.

**Body:**
```json
{
  "horarios": [
    {"dia_semana": 0, "jornada": "M", "sede": "SA"},
    {"dia_semana": 2, "jornada": "T", "sede": "BA"}
  ]
}
```

**Respuesta (200):**
```json
{
  "mensaje": "Se editaron los horarios exitosamente para monitor1",
  "horarios_eliminados": 5,
  "horarios_creados": [
    {
      "id": 6,
      "usuario": {...},
      "dia_semana": 0,
      "dia_semana_display": "Lunes",
      "jornada": "M",
      "jornada_display": "Mañana",
      "sede": "SA",
      "sede_display": "San Antonio"
    }
  ],
  "total_solicitados": 2,
  "total_creados": 2,
  "usuario": {
    "id": 1,
    "username": "monitor1",
    "nombre": "Juan Monitor"
  }
}
```

---

## 👨‍💼 Endpoints para Directivos

### Listar Horarios de Todos los Monitores
**GET** `/example/directivo/horarios/`

**Descripción:** Permite a los directivos ver todos los horarios fijos de todos los monitores del sistema con filtros opcionales.

**Headers:** `Authorization: Bearer <token>` (solo DIRECTIVO)

**Parámetros de consulta (opcionales):**
- `usuario_id`: ID específico del monitor (número entero)
- `dia_semana`: Día de la semana (0-6, donde 0=Lunes)
- `jornada`: Jornada (M=Mañana, T=Tarde)
- `sede`: Sede (SA=San Antonio, BA=Barcelona)

**Ejemplos de uso:**
```bash
# Todos los horarios de todos los monitores
GET /example/directivo/horarios/

# Horarios de un monitor específico
GET /example/directivo/horarios/?usuario_id=5

# Horarios de los lunes
GET /example/directivo/horarios/?dia_semana=0

# Horarios de mañana en San Antonio
GET /example/directivo/horarios/?jornada=M&sede=SA
```

**Respuesta Exitosa (200):**
```json
{
  "total_horarios": 15,
  "total_monitores": 8,
  "horarios": [
    {
      "id": 1,
      "usuario": {
        "id": 3,
        "username": "monitor1",
        "nombre": "Juan Monitor",
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
}
```

---

## 🔧 Ajustes Manuales de Horas (HU7A)

### Listar y Crear Ajustes de Horas
**GET/POST** `/example/directivo/ajustes-horas/`

**Descripción:** Permite a los directivos listar ajustes de horas existentes y crear nuevos ajustes para dar o quitar horas a monitores.

**Headers:** `Authorization: Bearer <token>` (solo DIRECTIVO)

#### GET - Listar Ajustes

**Parámetros de consulta (opcionales):**
- `monitor_id`: ID específico del monitor (número entero)
- `fecha_inicio`: Fecha de inicio del filtro (YYYY-MM-DD). Por defecto: 30 días atrás
- `fecha_fin`: Fecha de fin del filtro (YYYY-MM-DD). Por defecto: hoy

**Ejemplos de uso:**
```bash
# Todos los ajustes del último mes
GET /example/directivo/ajustes-horas/

# Ajustes de un monitor específico
GET /example/directivo/ajustes-horas/?monitor_id=3

# Ajustes en un período específico
GET /example/directivo/ajustes-horas/?fecha_inicio=2025-01-01&fecha_fin=2025-01-31
```

**Respuesta Exitosa (200):**
```json
{
  "periodo": {
    "fecha_inicio": "2025-01-01",
    "fecha_fin": "2025-01-31"
  },
  "estadisticas": {
    "total_ajustes": 5,
    "total_horas_ajustadas": 12.5,
    "monitores_afectados": 3
  },
  "filtros_aplicados": {
    "monitor_id": null
  },
  "ajustes": [
    {
      "id": 1,
      "usuario": {
        "id": 3,
        "username": "monitor1",
        "nombre": "Juan Monitor",
        "tipo_usuario": "MONITOR",
        "tipo_usuario_display": "Monitor"
      },
      "fecha": "2025-01-15",
      "cantidad_horas": "4.00",
      "motivo": "Recuperación por día perdido por enfermedad",
      "creado_por": {
        "id": 1,
        "username": "directivo1",
        "nombre": "María Directivo",
        "tipo_usuario": "DIRECTIVO",
        "tipo_usuario_display": "Directivo"
      },
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

---

#### POST - Crear Ajuste

**Body:**
```json
{
  "monitor_id": 3,
  "fecha": "2025-01-15",
  "cantidad_horas": 4.00,
  "motivo": "Recuperación por día perdido por enfermedad"
}
```

**Campos:**
- `monitor_id`: (requerido) ID del monitor al que se le ajustan las horas
- `fecha`: (requerido) Fecha del ajuste en formato YYYY-MM-DD
- `cantidad_horas`: (requerido) Cantidad de horas (positivo para agregar, negativo para restar). Rango: -24.00 a 24.00
- `motivo`: (requerido) Descripción del motivo del ajuste

**Validaciones:**
- `monitor_id` debe existir y ser de tipo MONITOR
- `cantidad_horas` no puede ser 0 y debe estar entre -24.00 y 24.00

**Respuesta Exitosa (201):**
```json
{
  "id": 1,
  "usuario": {
    "id": 3,
    "username": "monitor1",
    "nombre": "Juan Monitor",
    "tipo_usuario": "MONITOR",
    "tipo_usuario_display": "Monitor"
  },
  "fecha": "2025-01-15",
  "cantidad_horas": "4.00",
  "motivo": "Recuperación por día perdido por enfermedad",
  "creado_por": {
    "id": 1,
    "username": "directivo1",
    "nombre": "María Directivo",
    "tipo_usuario": "DIRECTIVO",
    "tipo_usuario_display": "Directivo"
  },
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

---

### Detalles y Eliminar Ajuste
**GET/DELETE** `/example/directivo/ajustes-horas/{id}/`

**Headers:** `Authorization: Bearer <token>` (solo DIRECTIVO)

#### GET - Obtener Detalles

**Respuesta Exitosa (200):**
```json
{
  "id": 1,
  "usuario": {
    "id": 3,
    "username": "monitor1",
    "nombre": "Juan Monitor",
    "tipo_usuario": "MONITOR",
    "tipo_usuario_display": "Monitor"
  },
  "fecha": "2025-01-15",
  "cantidad_horas": "4.00",
  "motivo": "Recuperación por día perdido por enfermedad",
  "creado_por": {
    "id": 1,
    "username": "directivo1",
    "nombre": "María Directivo",
    "tipo_usuario": "DIRECTIVO",
    "tipo_usuario_display": "Directivo"
  },
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

---

#### DELETE - Eliminar Ajuste

**Descripción:** Elimina un ajuste de horas. Útil para corregir errores.

**Respuesta Exitosa (204):**
```json
{
  "detail": "Ajuste de horas eliminado exitosamente"
}
```

---

## ⚙️ Configuraciones del Sistema (HU9)

### Listar Configuraciones
**GET** `/example/directivo/configuraciones/`

**Descripción:** Lista todas las configuraciones del sistema que pueden ser editadas por los directivos.

**Headers:** `Authorization: Bearer <token>` (solo DIRECTIVO)

**Respuesta Exitosa (200):**
```json
{
  "total_configuraciones": 2,
  "configuraciones": [
    {
      "id": 1,
      "clave": "costo_por_hora",
      "valor": "9965",
      "descripcion": "Costo por hora de trabajo de los monitores en pesos colombianos (COP)",
      "tipo_dato": "decimal",
      "valor_tipado": 9965.0,
      "creado_por": {
        "id": 1,
        "username": "directivo1",
        "nombre": "María Directivo",
        "tipo_usuario": "DIRECTIVO",
        "tipo_usuario_display": "Directivo"
      },
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "clave": "semanas_semestre",
      "valor": "14",
      "descripcion": "Total de semanas que dura un semestre académico",
      "tipo_dato": "entero",
      "valor_tipado": 14,
      "creado_por": {...},
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

---

### Crear Nueva Configuración
**POST** `/example/directivo/configuraciones/crear/`

**Descripción:** Crea una nueva configuración del sistema.

**Headers:** `Authorization: Bearer <token>` (solo DIRECTIVO)

**Body:**
```json
{
  "clave": "nueva_configuracion",
  "valor": "100",
  "descripcion": "Descripción de la nueva configuración",
  "tipo_dato": "entero"
}
```

**Campos:**
- `clave`: (requerido) Clave única para identificar la configuración (solo letras, números y guiones bajos)
- `valor`: (requerido) Valor de la configuración
- `descripcion`: (requerido) Descripción de qué representa esta configuración
- `tipo_dato`: (requerido) Tipo de dato: "decimal", "entero", "texto", "booleano"

**Respuesta Exitosa (201):**
```json
{
  "id": 3,
  "clave": "nueva_configuracion",
  "valor": "100",
  "descripcion": "Descripción de la nueva configuración",
  "tipo_dato": "entero",
  "valor_tipado": 100,
  "creado_por": {...},
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

---

### Inicializar Configuraciones por Defecto
**POST** `/example/directivo/configuraciones/inicializar/`

**Descripción:** Crea las configuraciones básicas del sistema (costo por hora y semanas del semestre) si no existen.

**Headers:** `Authorization: Bearer <token>` (solo DIRECTIVO)

**Respuesta Exitosa (201):**
```json
{
  "mensaje": "Se crearon 2 configuraciones nuevas",
  "configuraciones_creadas": [
    {
      "id": 1,
      "clave": "costo_por_hora",
      "valor": "9965",
      "descripcion": "Costo por hora de trabajo de los monitores en pesos colombianos (COP)",
      "tipo_dato": "decimal",
      "valor_tipado": 9965.0
    },
    {
      "id": 2,
      "clave": "semanas_semestre",
      "valor": "14",
      "descripcion": "Total de semanas que dura un semestre académico",
      "tipo_dato": "entero",
      "valor_tipado": 14
    }
  ],
  "configuraciones_existentes": [],
  "total_procesadas": 2
}
```

---

### Obtener/Actualizar/Eliminar Configuración
**GET/PUT/DELETE** `/example/directivo/configuraciones/{clave}/`

**Descripción:** Obtiene, actualiza o elimina una configuración específica por su clave.

**Headers:** `Authorization: Bearer <token>` (solo DIRECTIVO)

#### GET - Obtener Configuración

**Ejemplo:**
```bash
GET /example/directivo/configuraciones/costo_por_hora/
```

**Respuesta Exitosa (200):**
```json
{
  "id": 1,
  "clave": "costo_por_hora",
  "valor": "9965",
  "descripcion": "Costo por hora de trabajo de los monitores en pesos colombianos (COP)",
  "tipo_dato": "decimal",
  "valor_tipado": 9965.0,
  "creado_por": {...},
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

---

#### PUT - Actualizar Configuración

**Body:**
```json
{
  "clave": "costo_por_hora",
  "valor": "10000",
  "descripcion": "Costo por hora actualizado",
  "tipo_dato": "decimal"
}
```

**Respuesta (200):**
```json
{
  "id": 1,
  "clave": "costo_por_hora",
  "valor": "10000",
  "descripcion": "Costo por hora actualizado",
  "tipo_dato": "decimal",
  "valor_tipado": 10000.0,
  "creado_por": {...},
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-10-23T14:30:00Z"
}
```

---

#### DELETE - Eliminar Configuración

**Respuesta Exitosa (204):**
```json
{
  "detail": "Configuración eliminada exitosamente"
}
```

---

### Obtener/Actualizar/Eliminar Configuración por ID
**GET/PUT/DELETE** `/example/directivo/configuraciones/{id}/`

**Descripción:** Mismo comportamiento que el endpoint por clave, pero usando el ID numérico.

**Headers:** `Authorization: Bearer <token>` (solo DIRECTIVO)

---

## 📊 Códigos de Estado

- **200 OK**: Petición exitosa
- **201 Created**: Recurso creado exitosamente
- **204 No Content**: Recurso eliminado exitosamente
- **207 Multi-Status**: Operación masiva con algunos errores
- **400 Bad Request**: Error en los datos enviados
- **401 Unauthorized**: Token inválido o faltante
- **403 Forbidden**: Permisos insuficientes
- **404 Not Found**: Recurso no encontrado

---

## 🔧 Valores de los Campos

### Días de la Semana
- `0`: Lunes
- `1`: Martes
- `2`: Miércoles
- `3`: Jueves
- `4`: Viernes
- `5`: Sábado
- `6`: Domingo

### Jornadas
- `"M"`: Mañana (4 horas)
- `"T"`: Tarde (4 horas)

### Sedes
- `"SA"`: San Antonio
- `"BA"`: Barcelona

### Tipos de Usuario
- `"MONITOR"`: Monitor académico
- `"DIRECTIVO"`: Directivo administrativo

### Tipos de Dato (Configuraciones)
- `"decimal"`: Números decimales
- `"entero"`: Números enteros
- `"texto"`: Cadenas de texto
- `"booleano"`: Valores true/false

---

## 🚀 Ejemplos de Uso

### 1. Login y Obtener Token
```bash
curl -X POST http://localhost:8000/example/login/ \
  -H "Content-Type: application/json" \
  -d '{"password": "Admin#1234", "nombre_de_usuario": "superusuario"}'
```

### 2. Registrar Nuevo Monitor
```bash
curl -X POST http://localhost:8000/example/registro/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "monitor1",
    "nombre": "Juan Monitor",
    "password": "password123",
    "confirm_password": "password123"
  }'
```

### 3. Crear Horario Fijo
```bash
curl -X POST http://localhost:8000/example/horarios/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"dia_semana": 0, "jornada": "M", "sede": "SA"}'
```

### 4. Crear Múltiples Horarios
```bash
curl -X POST http://localhost:8000/example/horarios/multiple/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "horarios": [
      {"dia_semana": 0, "jornada": "M", "sede": "SA"},
      {"dia_semana": 2, "jornada": "T", "sede": "BA"},
      {"dia_semana": 4, "jornada": "M", "sede": "SA"}
    ]
  }'
```

### 5. Consultar Horarios (Directivo)
```bash
curl -X GET "http://localhost:8000/example/directivo/horarios/?jornada=M&sede=SA" \
  -H "Authorization: Bearer <token>"
```

### 6. Crear Ajuste de Horas (Directivo)
```bash
curl -X POST http://localhost:8000/example/directivo/ajustes-horas/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "monitor_id": 3,
    "fecha": "2025-10-22",
    "cantidad_horas": 2.5,
    "motivo": "Horas extra por evento especial"
  }'
```

### 7. Inicializar Configuraciones por Defecto
```bash
curl -X POST "http://localhost:8000/example/directivo/configuraciones/inicializar/" \
  -H "Authorization: Bearer <token>"
```

### 8. Actualizar Costo por Hora
```bash
curl -X PUT "http://localhost:8000/example/directivo/configuraciones/costo_por_hora/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "clave": "costo_por_hora",
    "valor": "10000",
    "descripcion": "Costo por hora actualizado",
    "tipo_dato": "decimal"
  }'
```

---

## 📝 Notas Importantes

- **Tokens JWT**: No expiran (configurados para duración extendida)
- **Autenticación**: Todos los endpoints excepto login y registro requieren token
- **Permisos**: 
  - Monitores: Pueden gestionar solo sus propios horarios
  - Directivos: Pueden consultar horarios de todos, crear ajustes y configurar el sistema
- **Validaciones**: 
  - Los horarios fijos son únicos por usuario, día y jornada
  - Los ajustes de horas tienen rango de -24 a 24 horas
  - Las configuraciones tienen validación según tipo de dato
- **Seguridad**: Contraseñas cifradas con pbkdf2_sha256

---

## 🔗 Base URL

**Desarrollo:** `http://localhost:8000/example/`

**Producción:** `https://tu-dominio.vercel.app/example/`

---

## 📚 Recursos Adicionales

- **Alcance del Proyecto:** Ver `ALCANCE_LABORATORIO_I.md`
- **Cambios Realizados:** Ver `CAMBIOS_LABORATORIO_I.md`
- **README:** Información general del proyecto
