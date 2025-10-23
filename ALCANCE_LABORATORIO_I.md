# Alcance del Laboratorio I
## Sistema de Monitoreo de Asistencias

### 📋 Contexto del Proyecto

**Producto**: Sistema de Monitoreo orientado a gestionar el ciclo completo de asistencia de monitores académicos bajo la supervisión de directivos.

**Usuarios previstos**: 
- Cuentas MONITOR
- Cuentas DIRECTIVO

---

## ✅ Alcance del Laboratorio I (IMPLEMENTADO)

### Funcionalidades Incluidas

#### HU1 - Registro de Monitor
**Endpoint**: `POST /example/registro/`
- Registro automático con rol MONITOR
- Generación automática de token JWT
- Validación de username único
- Contraseñas cifradas con hashing

#### HU2 - Login y Obtención de Token
**Endpoint**: `POST /example/login/`
- Autenticación JWT para monitores y directivos
- Token con lifetime extendido
- Retorna token y metadatos del usuario

#### HU3 - Gestión Individual de Horarios
**Endpoints**:
- `GET/POST /example/horarios/` - Listar y crear horarios
- `GET/PUT/DELETE /example/horarios/{id}/` - Operaciones individuales
- `POST /example/horarios/multiple/` - Creación masiva
- `PUT /example/horarios/edit-multiple/` - Edición masiva (reemplaza todos)
- `GET /example/directivo/horarios/` - Consulta directiva con filtros

**Características**:
- Días de la semana: 0-6 (Lunes-Domingo)
- Jornadas: M (Mañana), T (Tarde)
- Sedes: SA (San Antonio), BA (Barcelona)
- Validación de unicidad: usuario/día/jornada

#### HU7A - Ajustes Manuales de Horas
**Endpoints**:
- `GET/POST /example/directivo/ajustes-horas/` - Listar y crear ajustes
- `GET/DELETE /example/directivo/ajustes-horas/{id}/` - Operaciones por ID

**Características**:
- Rango de horas: -24.00 a 24.00
- Requiere motivo y monitor válido
- Trazabilidad completa (creador, fechas)
- Estadísticas del período

#### HU9 - Administración de Configuraciones del Sistema
**Endpoints**:
- `GET /example/directivo/configuraciones/` - Listar configuraciones
- `POST /example/directivo/configuraciones/crear/` - Crear configuración
- `POST /example/directivo/configuraciones/inicializar/` - Inicializar defaults
- `GET/PUT/DELETE /example/directivo/configuraciones/{clave}/` - Por clave
- `GET/PUT/DELETE /example/directivo/configuraciones/{id}/` - Por ID

**Características**:
- Tipos de dato: decimal, entero, texto, booleano
- Validaciones por tipo
- Configuraciones por defecto:
  - `costo_por_hora`: 9965 COP
  - `semanas_semestre`: 14

---

## 🚫 Fuera del Alcance Inmediato

Las siguientes funcionalidades NO están implementadas en el Laboratorio I y se desarrollarán en fases posteriores:

### ❌ HU4 - Marcaje de Asistencia por Monitor
- Endpoint de marcaje de asistencias
- Validación de jornadas autorizadas
- Cálculo automático de horas

### ❌ HU5 - Gestión Directiva de Asistencias
- Listado y filtrado de asistencias
- Autorización/rechazo de asistencias
- Generación automática de asistencias según horarios

### ❌ HU6 - Reportes de Horas
- Reporte individual por monitor
- Reporte consolidado de todos los monitores
- Estadísticas y métricas de horas trabajadas

### ❌ HU7B - Búsqueda Avanzada de Monitores
- Endpoint de búsqueda de monitores
- Filtros por nombre/username

### ❌ HU8 - Paneles Financieros
- Reporte financiero individual
- Reporte financiero consolidado
- Resumen ejecutivo
- Comparativa semanal
- Cálculos de costos y proyecciones

---

## 🗃️ Modelos de Base de Datos (Laboratorio I)

### UsuarioPersonalizado
- username (único)
- nombre
- password (hasheado)
- tipo_usuario (MONITOR/DIRECTIVO)
- is_active
- date_joined
- last_login

### HorarioFijo
- usuario (FK a UsuarioPersonalizado)
- dia_semana (0-6)
- jornada (M/T)
- sede (SA/BA)
- Unique constraint: (usuario, dia_semana, jornada)

### AjusteHoras
- usuario (FK a UsuarioPersonalizado - solo MONITOR)
- fecha
- cantidad_horas (-24 a 24, no puede ser 0)
- motivo (texto)
- creado_por (FK a UsuarioPersonalizado - solo DIRECTIVO)
- created_at
- updated_at

### ConfiguracionSistema
- clave (única)
- valor
- descripcion
- tipo_dato (decimal/entero/texto/booleano)
- creado_por (FK a UsuarioPersonalizado - solo DIRECTIVO)
- created_at
- updated_at

---

## 🔐 Seguridad y Autenticación

- **JWT**: Tokens con lifetime extendido
- **Hashing**: Contraseñas con pbkdf2_sha256
- **CORS**: Configurado para desarrollo (ajustable en producción)
- **Validaciones**: Integridad de datos en todos los endpoints

---

## 🛠️ Stack Tecnológico

- **Backend**: Django + Django REST Framework
- **Base de Datos**: PostgreSQL (configurable por variables de entorno)
- **Autenticación**: JWT (Simple JWT)
- **Despliegue**: Vercel (configurado con vercel.json)

---

## 📝 Próximos Pasos (Laboratorios Futuros)

1. **Laboratorio II**: Implementar asistencias (HU4, HU5)
2. **Laboratorio III**: Implementar reportes (HU6)
3. **Laboratorio IV**: Implementar paneles financieros (HU7B, HU8)

---

## 🚀 Cómo Usar el Sistema

### 1. Registro de Monitor
```bash
POST /example/registro/
{
  "username": "monitor1",
  "nombre": "Juan Pérez",
  "password": "password123",
  "confirm_password": "password123"
}
```

### 2. Login
```bash
POST /example/login/
{
  "nombre_de_usuario": "monitor1",
  "password": "password123"
}
```

### 3. Gestionar Horarios
```bash
# Crear horario
POST /example/horarios/
Authorization: Bearer {token}
{
  "dia_semana": 0,
  "jornada": "M",
  "sede": "SA"
}

# Listar horarios
GET /example/horarios/
Authorization: Bearer {token}
```

### 4. Ajustes de Horas (Directivo)
```bash
# Crear ajuste
POST /example/directivo/ajustes-horas/
Authorization: Bearer {token_directivo}
{
  "monitor_id": 1,
  "fecha": "2025-10-22",
  "cantidad_horas": 2.5,
  "motivo": "Horas extra por evento especial"
}
```

### 5. Configuraciones (Directivo)
```bash
# Inicializar configuraciones por defecto
POST /example/directivo/configuraciones/inicializar/
Authorization: Bearer {token_directivo}

# Listar configuraciones
GET /example/directivo/configuraciones/
Authorization: Bearer {token_directivo}
```

---

## 📚 Documentación Adicional

- `API_DOCUMENTATION.md` - Documentación completa de endpoints
- `FRONTEND_CONFIG.md` - Configuración para frontend
- `GUIA_FINANZAS.md` - Guía de módulos financieros (para futuras fases)
- `README.md` - Información general del proyecto

