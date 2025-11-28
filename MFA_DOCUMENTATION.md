# Documentación de Implementación MFA (Multi-Factor Authentication)

## 📋 Resumen General

Se ha implementado un sistema completo de **Autenticación en Dos Factores (MFA)** en tu proyecto Django NUAM. El sistema soporta dos métodos:

1. **OTP por Email**: Códigos de 6 dígitos válidos por 10 minutos
2. **TOTP (Time-based One-Time Password)**: Códigos generados por apps de autenticación (Google Authenticator, Authy, Microsoft Authenticator)

---

## 🔧 Cambios Realizados

### 1. **Modelo de Usuario (`cuentas/models.py`)**

Se agregaron 5 nuevos campos al modelo `Usuario`:

```python
mfa_enabled = BooleanField(default=False)           # ¿MFA está habilitado?
mfa_secret = CharField(max_length=32, null=True)    # Clave secreta TOTP
otp_code = CharField(max_length=6, null=True)       # Código OTP actual
otp_created_at = DateTimeField(null=True)           # Cuándo se generó el OTP
backup_codes = TextField(null=True)                 # Códigos de respaldo (JSON)
```

**Nuevos Métodos:**

- `generate_otp()`: Genera un código de 6 dígitos válido por 10 minutos
- `verify_otp(code)`: Verifica que el código OTP sea correcto y no haya expirado
- `get_totp_uri()`: Genera la URI para el código QR (compatible con Google Authenticator)
- `verify_totp(code)`: Verifica un código TOTP del autenticador

---

### 2. **Vistas (`cuentas/views.py`)**

Se agregaron 3 nuevas funciones:

#### `verificar_mfa(request)`
- Verifica el código OTP enviado por email durante el login
- Si el código es correcto, completa el login
- Maneja códigos expirados o incorrectos

#### `habilitar_mfa(request)`
- Permite al usuario habilitar/deshabilitar MFA
- Genera QR para Google Authenticator
- Muestra la clave secreta de respaldo
- Verifica que el usuario ingrese el código correcto antes de activar

#### `inicio_sesion()` - ACTUALIZADO
- Ahora detecta si el usuario tiene MFA habilitado
- Envía OTP por email si MFA está activo
- Redirige a página de verificación

---

### 3. **URLs (`cuentas/urls.py`)**

Se agregaron dos nuevas rutas:

```python
path('verificar-mfa/', views.verificar_mfa, name='verificar_mfa')
path('habilitar-mfa/', views.habilitar_mfa, name='habilitar_mfa')
```

---

### 4. **Templates**

#### `verificar_mfa.html`
- Interfaz para ingresar el código OTP
- Diseño moderno con gradiente púrpura-rosa-rojo
- Muestra el email donde se envió el código
- Opción para volver al login

#### `habilitar_mfa.html`
- Pantalla para configurar MFA en la cuenta
- Muestra código QR para scanear
- Muestra clave secreta de respaldo
- Permite habilitar/deshabilitar MFA
- Interfaz responsiva con dos paneles

---

### 5. **Configuración (`mantenedornuam/settings.py`)**

Se agregó configuración de correo:

```python
# Para desarrollo (muestra los correos en consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Para producción con Gmail (descomenta y configura):
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = 'noreply@nuam.com'
```

---

## 🚀 Cómo Usar MFA

### **Para Usuarios Finales:**

1. **Habilitar MFA:**
   - Ir a Dashboard
   - Hacer clic en el icono de escudo (🛡️) en la barra superior
   - Hacer clic en "Habilitar MFA"
   - Escanear el código QR con Google Authenticator o Authy
   - Ingresar el código de 6 dígitos para confirmar

2. **Iniciar Sesión con MFA:**
   - Ingresar correo y contraseña normalmente
   - Se enviará un código a tu correo
   - Ingresar el código en la pantalla de verificación
   - ¡Sesión iniciada!

3. **Deshabilitar MFA:**
   - Ir a Dashboard → Configurar MFA
   - Hacer clic en "Deshabilitar MFA"

---

## 🛠️ Instalación y Configuración

### **1. Instalar paquetes necesarios:**

```bash
pip install pyotp qrcode[pil]
```

### **2. Crear las migraciones:**

```bash
python manage.py makemigrations cuentas
python manage.py migrate cuentas
```

### **3. Configurar correo (Opcional para producción):**

Si deseas usar Gmail en producción:

1. Habilitar [Contraseñas de Aplicación de Google](https://myaccount.google.com/apppasswords)
2. Agregar a `.env`:
   ```
   EMAIL_HOST_USER=tu_email@gmail.com
   EMAIL_HOST_PASSWORD=tu_contraseña_app
   ```
3. Descomentar la configuración SMTP en `settings.py`

---

## 📊 Flujo de Autenticación

```
┌─────────────────┐
│  Login Page     │
│  Email + Pass   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Verificar Email y Contraseña        │
│ check_password(password)             │
└────────┬────────────────────────────┘
         │
         ├─── ¿MFA Habilitado? ───NO──→ ✅ LOGIN COMPLETADO
         │
         YES
         │
         ▼
┌──────────────────────────┐
│ Generar OTP              │
│ generate_otp()           │
│ Enviar por Email         │
│ send_mail()              │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Pantalla de Verificación│
│  Ingresar OTP (6 dígitos)│
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Verificar OTP            │
│ verify_otp(code)         │
│ - Código correcto?       │
│ - No expirado?           │
└────────┬─────────────────┘
         │
    ┌────┴────┐
    │          │
   SÍ         NO
    │          │
    ▼          ▼
✅ LOGIN    ❌ ERROR
   COMPLETADO
```

---

## 🔐 Seguridad

### Características de Seguridad Implementadas:

1. **OTP con Expiración**: Los códigos expiran después de 10 minutos
2. **TOTP Basado en Tiempo**: Compatible con estándares RFC 6238
3. **Códigos de Respaldo**: Usuarios pueden guardar clave secreta
4. **Sin Almacenamiento de Códigos**: Los códigos no se guardan en BD
5. **Validación de Entrada**: Validación de código de 6 dígitos

---

## 📱 Apps de Autenticación Compatibles

- **Google Authenticator** (Android/iOS)
- **Microsoft Authenticator** (Android/iOS)
- **Authy** (Android/iOS/Desktop)
- **1Password** (Android/iOS)
- **LastPass Authenticator** (Android/iOS)

---

## 🐛 Resolución de Problemas

### "ModuleNotFoundError: No module named 'pyotp'"
```bash
pip install pyotp qrcode[pil]
```

### "Los correos no se envían"
Verifica que `EMAIL_BACKEND` sea el correcto en `settings.py`

### "El código QR no aparece"
Asegúrate de tener `qrcode[pil]` instalado:
```bash
pip install qrcode[pil]
```

### "El código expira muy rápido"
El tiempo de expiración está configurado a 10 minutos en `models.py`:
```python
otp_created_at.add(minutes=10) > timezone.now()
```

---

## 📝 Archivos Modificados

✅ `cuentas/models.py` - Agregados campos y métodos MFA
✅ `cuentas/views.py` - Vistas para MFA
✅ `cuentas/urls.py` - Rutas para MFA
✅ `cuentas/templates/verificar_mfa.html` - Template de verificación
✅ `cuentas/templates/habilitar_mfa.html` - Template de configuración
✅ `mantenedornuam/settings.py` - Configuración de email
✅ `dashboard/templates/dashboard.html` - Botón para acceder a MFA

---

## 🔄 Próximas Mejoras (Opcional)

1. **Backup Codes**: Generar códigos de respaldo para recuperación
2. **Recuperación por Email**: Enviar link de recuperación si se pierde el autenticador
3. **SMS OTP**: Agregar soporte para códigos por SMS
4. **Admin Interface**: Panel de administración para gestionar MFA de usuarios
5. **Notificaciones**: Alertas cuando se habilita/deshabilita MFA
6. **Auditoría**: Log de intentos de login y cambios de MFA

---

## 📞 Soporte

Para preguntas o problemas con la implementación de MFA, consulta:
- Documentación de PyOTP: https://github.com/pyauth/pyotp
- Documentación de Django Email: https://docs.djangoproject.com/en/stable/topics/email/
- RFC 6238 (TOTP): https://tools.ietf.org/html/rfc6238

---

**Última actualización:** 2024
**Estado:** ✅ Implementado y Funcional
