# Sistema de Monitoreo de Asistencias - Backend (Laboratorio I)

Backend del Sistema de Monitoreo orientado a gestionar el ciclo completo de asistencia de monitores académicos bajo la supervisión de directivos.

## 🎯 Alcance Actual: Laboratorio I

El proyecto actualmente implementa las funcionalidades base del sistema:

### ✅ Implementado

- **HU1**: Registro de monitores con token automático
- **HU2**: Login y autenticación JWT
- **HU3**: Gestión de horarios (individual y masiva)
- **HU7A**: Ajustes manuales de horas
- **HU9**: Administración de configuraciones del sistema

### ⏳ Pendiente (Futuros Laboratorios)

- **HU4, HU5**: Gestión de asistencias (marcaje, autorización)
- **HU6**: Reportes de horas (individual y consolidado)
- **HU7B, HU8**: Paneles financieros y comparativas

📄 Ver [`ALCANCE_LABORATORIO_I.md`](ALCANCE_LABORATORIO_I.md) para detalles completos del alcance.

---

## 🛠️ Stack Tecnológico

- **Framework**: Django 4.x + Django REST Framework
- **Base de Datos**: PostgreSQL
- **Autenticación**: JWT (djangorestframework-simplejwt)
- **Despliegue**: Vercel con Serverless Functions

---

## 📦 Instalación y Configuración

### Requisitos Previos

- Python 3.9+
- PostgreSQL
- pip

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd devops-back
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de datos
DB_NAME=nombre_base_datos
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
```

### 4. Aplicar Migraciones

```bash
python manage.py migrate
```

### 5. Crear Usuario Directivo (Opcional)

```bash
python crear_usuario.py
```

### 6. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

---

## 🚀 Uso del API

### Autenticación

#### Registro de Monitor
```bash
POST /example/registro/
Content-Type: application/json

{
  "username": "monitor1",
  "nombre": "Juan Pérez",
  "password": "password123",
  "confirm_password": "password123"
}
```

#### Login
```bash
POST /example/login/
Content-Type: application/json

{
  "nombre_de_usuario": "monitor1",
  "password": "password123"
}
```

### Horarios

#### Crear Horario Individual
```bash
POST /example/horarios/
Authorization: Bearer <token>
Content-Type: application/json

{
  "dia_semana": 0,
  "jornada": "M",
  "sede": "SA"
}
```

#### Crear Múltiples Horarios
```bash
POST /example/horarios/multiple/
Authorization: Bearer <token>
Content-Type: application/json

{
  "horarios": [
    {"dia_semana": 0, "jornada": "M", "sede": "SA"},
    {"dia_semana": 2, "jornada": "T", "sede": "BA"}
  ]
}
```

### Ajustes de Horas (Directivo)

```bash
POST /example/directivo/ajustes-horas/
Authorization: Bearer <token_directivo>
Content-Type: application/json

{
  "monitor_id": 1,
  "fecha": "2025-10-22",
  "cantidad_horas": 2.5,
  "motivo": "Horas extra por evento especial"
}
```

### Configuraciones (Directivo)

```bash
# Inicializar configuraciones por defecto
POST /example/directivo/configuraciones/inicializar/
Authorization: Bearer <token_directivo>

# Listar configuraciones
GET /example/directivo/configuraciones/
Authorization: Bearer <token_directivo>
```

---

## 📚 Documentación

- [`API_DOCUMENTATION.md`](API_DOCUMENTATION.md) - Documentación completa de endpoints
- [`ALCANCE_LABORATORIO_I.md`](ALCANCE_LABORATORIO_I.md) - Alcance detallado del Laboratorio I
- [`FRONTEND_CONFIG.md`](FRONTEND_CONFIG.md) - Configuración para integración frontend
- [`GUIA_FINANZAS.md`](GUIA_FINANZAS.md) - Guía de módulos financieros (futuros)

---

## 🗃️ Estructura del Proyecto

```
devops-back/
├── api/                    # Configuración de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── example/                # Aplicación principal
│   ├── models.py          # Modelos: Usuario, Horario, Ajuste, Config
│   ├── views.py           # Vistas del API
│   ├── serializers.py     # Serializers de DRF
│   ├── urls.py            # URLs de la aplicación
│   └── migrations/        # Migraciones de base de datos
├── requirements.txt       # Dependencias Python
├── vercel.json           # Configuración de Vercel
└── README.md             # Este archivo
```

---

## 🔐 Seguridad

- **Contraseñas**: Hasheadas con pbkdf2_sha256
- **JWT**: Tokens con lifetime extendido
- **Validaciones**: Integridad de datos en todos los endpoints
- **CORS**: Configurado para desarrollo (ajustable en producción)

---

## 🚀 Despliegue en Vercel

### Configuración

El proyecto incluye un archivo `vercel.json` preconfigurado.

### Deploy

```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel
```

O usar el botón de deploy:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=YOUR_REPO_URL)

---

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Test de conexión a BD
python test_db_connection.py
```

---

## 👥 Roles y Permisos

### Monitor
- ✅ Registro y login
- ✅ Gestión de sus propios horarios
- ❌ No puede acceder a endpoints de directivos

### Directivo
- ✅ Login
- ✅ Consulta de horarios de todos los monitores
- ✅ Gestión de ajustes de horas
- ✅ Administración de configuraciones

---

## 🔄 Próximas Fases

### Laboratorio II
- Implementar marcaje de asistencias (HU4)
- Implementar gestión directiva de asistencias (HU5)

### Laboratorio III
- Implementar reportes de horas (HU6)

### Laboratorio IV
- Implementar búsqueda avanzada de monitores (HU7B)
- Implementar paneles financieros (HU8)

---

## 📝 Scripts Útiles

### Crear Usuario Directivo
```bash
python crear_usuario.py
```

### Resetear Base de Datos
```bash
python reset_database.py
```

### Test de Conexión
```bash
python test_db_connection.py
```

---

## 📄 Licencia

Este proyecto es parte del curso de DevOps y está bajo la supervisión académica correspondiente.

---

## 🤝 Contribuciones

Este es un proyecto académico. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📧 Contacto

Para preguntas o soporte técnico, contactar al equipo de desarrollo del proyecto.
