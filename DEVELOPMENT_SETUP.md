# 🛠️ INSTRUCCIONES DE DESARROLLO - MFA

## Paso 1: Instalar Dependencias

Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
# Asegúrate de estar en la carpeta correcta
cd c:\Users\M0PA\Documents\GitHub\Proyecto-nuam

# Activar virtual environment (si no está activado)
venv\Scripts\activate

# Instalar pyotp y qrcode
pip install pyotp qrcode[pil]
```

---

## Paso 2: Crear Migraciones

```bash
# Crear los archivos de migración basados en los cambios del modelo
python manage.py makemigrations cuentas

# Deberías ver algo como:
# Migrations for 'cuentas':
#   cuentas/migrations/0006_usuario_mfa_fields.py
#     - Add field mfa_enabled to usuario
#     - Add field mfa_secret to usuario
#     - Add field otp_code to usuario
#     - Add field otp_created_at to usuario
#     - Add field backup_codes to usuario
```

---

## Paso 3: Ejecutar Migraciones

```bash
# Aplicar las migraciones a la base de datos
python manage.py migrate cuentas

# Deberías ver algo como:
# Operations to perform:
#   Apply all migrations: cuentas
# Running migrations:
#   Applying cuentas.0006_usuario_mfa_fields... OK
```

---

## Paso 4: Iniciar el Servidor

```bash
# Inicia el servidor de desarrollo
python manage.py runserver

# Deberías ver algo como:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CTRL-BREAK.
```

---

## Paso 5: Probar la Funcionalidad

### 5.1 Crear un Usuario de Prueba

1. Ve a: `http://localhost:8000/cuentas/register/`
2. Completa el formulario:
   - Nombre: Test User
   - Email: test@example.com
   - Contraseña: TestPassword123!

### 5.2 Probar Login Normal (sin MFA)

1. Ve a: `http://localhost:8000/cuentas/login/`
2. Inicia sesión con las credenciales del usuario
3. Deberías ir al dashboard sin necesidad de código

### 5.3 Habilitar MFA

1. En el dashboard, haz clic en el icono de escudo 🛡️
2. Haz clic en "Habilitar MFA"
3. **Importante**: Necesitas Google Authenticator o similar
   - Descárgalo: https://apps.apple.com/app/id388497605 (iOS)
   - Descárgalo: https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2 (Android)
4. Escanea el QR code que aparece
5. Ingresa el código de 6 dígitos en la pantalla
6. Haz clic en "Confirmar y Habilitar"

### 5.4 Probar Login con MFA

1. Cierra la sesión (click en "Salir")
2. Ve a: `http://localhost:8000/cuentas/login/`
3. Inicia sesión con email y contraseña
4. **En la terminal verás el código OTP** (por estar en modo console)
   ```
   ---------------
   Content-Type: text/plain; charset="utf-8"
   MIME-Version: 1.0
   Content-Transfer-Encoding: 7bit
   Subject: Código de verificación MFA - NUAM
   From: noreply@nuam.com
   To: test@example.com
   Date: ...
   
   Tu código de verificación es: 451289
   
   Este código es válido por 10 minutos.
   ---------------
   ```
5. Copia el código (ejemplo: 451289)
6. Ingresa el código en la pantalla
7. ¡Deberías estar en el dashboard!

### 5.5 Deshabilitar MFA

1. En el dashboard, haz clic en el icono de escudo 🛡️
2. Haz clic en "Deshabilitar MFA"
3. Confirmado

---

## 📋 Checklist de Pruebas

### Funcionalidades Base
- [ ] Usuario puede registrarse
- [ ] Usuario puede iniciar sesión sin MFA
- [ ] Usuario puede acceder al dashboard

### Funcionalidades MFA
- [ ] Usuario puede habilitar MFA
- [ ] QR code se genera correctamente
- [ ] Google Authenticator escanea el QR
- [ ] Código TOTP funciona en Google Authenticator
- [ ] Usuario puede verificar el código TOTP
- [ ] MFA se habilita en la base de datos
- [ ] Usuario puede desactivar MFA
- [ ] MFA se desactiva en la base de datos

### Login con MFA
- [ ] Al iniciar sesión con MFA, se envía OTP
- [ ] El código OTP aparece en la terminal
- [ ] Usuario puede ingresar el código
- [ ] El código correcto permite login
- [ ] El código incorrecto muestra error
- [ ] El código expirado (>10 min) muestra error

### Interfaz y Diseño
- [ ] Templates se ven modernos
- [ ] Gradientes se aplican correctamente
- [ ] Iconos de Font Awesome aparecen
- [ ] Diseño es responsive en móvil
- [ ] Mensajes de error se muestran
- [ ] Mensajes de éxito se muestran

---

## 🐛 Resolución de Problemas en Desarrollo

### Problema: "ModuleNotFoundError: No module named 'pyotp'"

**Solución:**
```bash
pip install pyotp
```

### Problema: "No se ve el código QR"

**Solución:**
```bash
pip install qrcode[pil]
```

### Problema: "El código OTP no aparece en la terminal"

**Causa:** EMAIL_BACKEND configurado incorrectamente
**Solución:** Verifica en `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Problema: "Migration conflicts"

**Solución:**
```bash
# Ver migraciones aplicadas
python manage.py showmigrations cuentas

# Si necesitas limpiar (SOLO en desarrollo)
# Borra la base de datos y crea nuevamente
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Problema: "El QR no se puede escanear"

**Causa:** PIL (Pillow) no instalada
**Solución:**
```bash
pip install Pillow
pip install qrcode[pil]
```

---

## 💾 Archivos Generados en BD

Después de las migraciones, se crearán en tu `db.sqlite3`:

```sql
-- Nueva tabla con campos MFA
ALTER TABLE cuentas_usuario
ADD COLUMN mfa_enabled BOOLEAN NOT NULL DEFAULT 0;

ALTER TABLE cuentas_usuario
ADD COLUMN mfa_secret VARCHAR(32);

ALTER TABLE cuentas_usuario
ADD COLUMN otp_code VARCHAR(6);

ALTER TABLE cuentas_usuario
ADD COLUMN otp_created_at DATETIME;

ALTER TABLE cuentas_usuario
ADD COLUMN backup_codes TEXT;
```

---

## 🔍 Comandos Útiles para Debugging

### Ver estado de las migraciones
```bash
python manage.py showmigrations cuentas
```

### Aplicar una migración específica
```bash
python manage.py migrate cuentas 0005
```

### Revertir una migración
```bash
python manage.py migrate cuentas 0005
```

### Ver esquema de la base de datos
```bash
python manage.py sqlmigrate cuentas 0006
```

### Abrir shell de Django
```bash
python manage.py shell

# Luego puedes hacer pruebas:
from cuentas.models import Usuario
u = Usuario.objects.first()
print(u.mfa_enabled)  # False
otp = u.generate_otp()
print(otp)  # Código OTP generado
```

---

## 📊 Estructura de Datos en BD

```
Tabla: cuentas_usuario
┌──────────────────────────────────────────┐
│ id (PK)                                  │
│ nombre (VARCHAR)                         │
│ correo (VARCHAR UNIQUE)                  │
│ password (VARCHAR hashed)                │
│ is_active (BOOLEAN)                      │
│ is_staff (BOOLEAN)                       │
├──────────────────────────────────────────┤
│ CAMPOS MFA (NUEVOS):                     │
│ mfa_enabled (BOOLEAN, DEFAULT=FALSE)     │
│ mfa_secret (VARCHAR 32, NULL)            │
│ otp_code (VARCHAR 6, NULL)               │
│ otp_created_at (DATETIME, NULL)          │
│ backup_codes (TEXT, NULL)                │
└──────────────────────────────────────────┘
```

---

## 🔐 Flujo de Datos Sensibles

```
1. CONTRASEÑA
   Usuario ingresa: "TestPassword123!"
   Django hashea: make_password("TestPassword123!")
   BD guarda: "pbkdf2_sha256$..."
   Login verifica: check_password()

2. OTP
   Sistema genera: generate_otp() → "451289"
   BD guarda temporalmente: otp_code = "451289"
   Email envía: send_mail() → "Tu código: 451289"
   Usuario ingresa: "451289"
   Sistema verifica: verify_otp("451289")
   BD limpia: otp_code = NULL

3. TOTP SECRET
   Sistema genera: pyotp.random_base32() → "JBSWY3DPE..."
   BD guarda: mfa_secret = "JBSWY3DPE..."
   QR genera: provisioning_uri(name, issuer)
   Usuario: Escanea con Google Authenticator
   Validación: verify_totp() verifica token actual
```

---

## 📈 Monitoreo en Desarrollo

### Ver logs en tiempo real
```bash
python manage.py runserver --verbosity 2
```

### Ver todas las consultas a BD
```python
# En settings.py, agregar:
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

## ✅ Checklist Final

- [ ] Dependencias instaladas (`pyotp`, `qrcode`)
- [ ] Migraciones creadas (`makemigrations`)
- [ ] Migraciones ejecutadas (`migrate`)
- [ ] Servidor inicia sin errores
- [ ] Usuario de prueba creado
- [ ] Login funciona sin MFA
- [ ] MFA puede habilitarse
- [ ] Google Authenticator genera códigos
- [ ] Login funciona con MFA
- [ ] MFA puede deshabilitarse
- [ ] Documentación leída
- [ ] Listo para producción

---

**¡Listo para desarrollar! 🚀**

Si tienes dudas, consulta los archivos de documentación generados.
