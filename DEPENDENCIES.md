# 📦 DEPENDENCIAS DEL PROYECTO NUAM

## Resumen General

El proyecto NUAM requiere las siguientes dependencias para funcionar correctamente:

---

## 🔧 Dependencias Principales

### Django Framework
```
Django>=3.2,<5.0
```
- **Propósito**: Framework web principal
- **Versión**: Compatible con Django 3.2, 4.x
- **Uso**: ORM, Vistas, Templates, Autenticación

### Web Server
```
gunicorn>=20.1.0
```
- **Propósito**: Servidor WSGI para producción
- **Uso**: Deploy en servidor
- **Comando**: `gunicorn mantenedornuam.wsgi`

### Database - PostgreSQL
```
psycopg2-binary>=2.9.0
```
- **Propósito**: Adaptador PostgreSQL para Django
- **Uso**: Conexión a base de datos PostgreSQL
- **Nota**: `psycopg2-binary` evita necesidad de compilar

### Environment Variables
```
python-dotenv>=0.19.0
```
- **Propósito**: Cargar variables de .env
- **Uso**: Configuración segura de credenciales
- **Ejemplo**: `load_dotenv()` carga archivo .env

### Static Files Management
```
whitenoise>=6.0.0
```
- **Propósito**: Servir archivos estáticos en producción
- **Uso**: CSS, JS, imágenes sin servidor web adicional
- **Middleware**: Agregado en settings.py

---

## 🔐 MFA - Multi-Factor Authentication (NUEVO)

### OTP/TOTP Generation
```
pyotp>=2.8.0
```
- **Propósito**: Generar OTP (One-Time Password)
- **Uso**: Códigos de 6 dígitos por email y TOTP para Google Authenticator
- **Métodos**:
  - `pyotp.random_base32()` - Generar secreto
  - `pyotp.TOTP(secret)` - Generar códigos TOTP

### QR Code Generation
```
qrcode>=7.4.0
Pillow>=9.0.0
```
- **Propósito**: Generar códigos QR
- **Uso**: Para que usuarios escaneen con Google Authenticator
- **Dependencia**: Pillow (PIL) es requerida para generar imágenes

---

## 📊 Data Handling

### Excel File Support
```
openpyxl>=3.7.0
```
- **Propósito**: Lectura/escritura de archivos XLSX
- **Uso**: Carga masiva de calificaciones
- **Feature**: Dashboard → Carga de datos

---

## 🧪 Testing & Quality (Opcional - Desarrollo)

### Testing Framework
```
pytest>=7.0.0
pytest-django>=4.5.0
```
- **Propósito**: Testing del código
- **Instalación**: `pip install -r requirements-dev.txt`
- **Uso**: `pytest` para correr tests

### Code Quality
```
black>=22.0.0
flake8>=4.0.0
isort>=5.10.0
```
- **Propósito**: Linting y formateo
- **Uso**:
  - `black .` - Formateo automático
  - `flake8 .` - Linting
  - `isort .` - Organizar imports

---

## 🔒 Security & Utilities

### CORS Headers
```
django-cors-headers>=3.11.0
```
- **Propósito**: Manejo de CORS en producción
- **Uso**: Si tienes frontend separado en otro dominio

### HTTP Requests
```
requests>=2.28.0
```
- **Propósito**: Hacer requests HTTP
- **Uso**: Llamadas a APIs externas si fuera necesario

---

## 📋 Instalación Rápida

### Opción 1: Instalar todo de una vez
```bash
pip install -r requirements.txt
```

### Opción 2: Instalar solo producción
```bash
pip install -r requirements.txt
# Excluye: pytest, black, flake8, isort (opcionales)
```

### Opción 3: Instalar MFA específicamente
```bash
pip install pyotp qrcode[pil]
```

---

## 🚀 Setup Completo

```bash
# 1. Crear virtual environment
python -m venv venv

# 2. Activar virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear archivo .env
copy .env.example .env

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superuser (opcional)
python manage.py createsuperuser

# 7. Iniciar servidor
python manage.py runserver
```

---

## 📊 Compatibilidad de Versiones

| Dependencia | Versión Mínima | Versión Máxima | Razón |
|---|---|---|---|
| Django | 3.2 | <5.0 | Compatibilidad con ORM y features |
| gunicorn | 20.1.0 | Latest | WSGI server moderno |
| python-dotenv | 0.19.0 | Latest | Funcionalidad estable |
| psycopg2 | 2.9.0 | Latest | PostgreSQL driver actualizado |
| whitenoise | 6.0.0 | Latest | Static files en producción |
| openpyxl | 3.7.0 | Latest | Excel file handling |
| pyotp | 2.8.0 | Latest | OTP/TOTP generation |
| qrcode | 7.4.0 | Latest | QR code generation |
| Pillow | 9.0.0 | Latest | Image processing |

---

## ✅ Verificación de Instalación

Después de instalar, puedes verificar:

```bash
# Ver todas las dependencias instaladas
pip list

# Ver dependencias del proyecto
pip list | grep -E "(Django|pyotp|qrcode|openpyxl|gunicorn)"

# Verificar versiones específicas
python -c "import django; print(f'Django {django.VERSION}')"
python -c "import pyotp; print(f'PyOTP {pyotp.__version__}')"
python -c "import qrcode; print(f'QRCode {qrcode.__version__}')"
```

---

## 🔄 Actualizar Dependencias

```bash
# Actualizar una dependencia específica
pip install --upgrade Django

# Actualizar todas las dependencias
pip install --upgrade -r requirements.txt

# Generar nuevo requirements.txt con versiones actuales
pip freeze > requirements.txt
```

---

## 🚨 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pyotp'"
```bash
pip install pyotp
```

### Error: "No module named 'qrcode'"
```bash
pip install qrcode[pil]
```

### Error: "psycopg2 compile error"
```bash
# Usar binary version
pip install psycopg2-binary
```

### Error: "Pillow not installed"
```bash
pip install Pillow
```

### Virtual Environment no activado
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

---

## 📦 Archivos de Dependencias

### requirements.txt
- Todas las dependencias de **producción y desarrollo**
- Incluye versiones pinned para estabilidad
- Usar: `pip install -r requirements.txt`

### requirements-prod.txt (Opcional crear)
```bash
django>=3.2,<5.0
gunicorn>=20.1.0
psycopg2-binary>=2.9.0
python-dotenv>=0.19.0
whitenoise>=6.0.0
openpyxl>=3.7.0
pyotp>=2.8.0
qrcode>=7.4.0
Pillow>=9.0.0
django-cors-headers>=3.11.0
requests>=2.28.0
```

### requirements-dev.txt (Opcional crear)
```bash
-r requirements.txt
pytest>=7.0.0
pytest-django>=4.5.0
black>=22.0.0
flake8>=4.0.0
isort>=5.10.0
```

---

## 🎯 Instalación por Caso de Uso

### Caso 1: Desarrollo Local
```bash
pip install -r requirements.txt
```
Instala todo incluyendo testing y quality tools.

### Caso 2: Producción
```bash
# Crear requirements-prod.txt sin testing tools
pip install -r requirements-prod.txt
```

### Caso 3: Solo MFA
```bash
pip install pyotp qrcode[pil] Pillow
```

### Caso 4: Solo Dashboard
```bash
pip install Django openpyxl gunicorn
```

---

## 📝 Notas Importantes

1. **Virtual Environment**: Siempre usa venv, nunca instales globalmente
2. **Versiones Pinned**: `requirements.txt` tiene versiones específicas para reproducibilidad
3. **PostgreSQL**: El proyecto usa PostgreSQL, configurar en `.env`
4. **SQLite**: Para desarrollo local se puede usar SQLite
5. **MFA**: Requiere `pyotp` + `qrcode[pil]` + `Pillow`
6. **Email**: Usar variables de `.env` para SMTP credentials

---

## 🔗 Links de Referencia

- [Django Documentation](https://docs.djangoproject.com/)
- [PyOTP GitHub](https://github.com/pyauth/pyotp)
- [QRCode Library](https://github.com/lincolnloop/python-qrcode)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Gunicorn Documentation](https://gunicorn.org/)

---

**Versión**: 1.0  
**Última Actualización**: 2024  
**Estado**: ✅ Completo
