from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils import timezone
from datetime import timedelta
import pyotp

# Create your models here.
class Usuario(AbstractBaseUser, models.Model):

    nombre =  models.CharField(max_length = 100)
    correo = models.EmailField(unique = True)
    password = models.CharField(max_length= 250)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Campos para MFA
    mfa_enabled = models.BooleanField(default=False)  # ¿MFA está activo?
    mfa_secret = models.CharField(max_length=32, blank=True, null=True)  # Secreto para autenticador
    otp_code = models.CharField(max_length=6, blank=True, null=True)  # Código OTP temporal
    otp_created_at = models.DateTimeField(blank=True, null=True)  # Cuándo se creó el OTP
    backup_codes = models.TextField(blank=True, null=True)  # Códigos de respaldo (JSON)
    
    USERNAME_FIELD = 'correo'

    objects = UserManager()
    
    def generate_otp(self):
        """Genera un código OTP de 6 dígitos válido por 10 minutos"""
        import random
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.otp_code = code
        self.otp_created_at = timezone.now()
        self.save()
        return code
    
    def verify_otp(self, code):
        """Verifica si el código OTP es correcto y no ha expirado"""
        if not self.otp_code or self.otp_code != code:
            return False
        
        # Verificar que no haya expirado (10 minutos)
        if timezone.now() - self.otp_created_at > timedelta(minutes=10):
            return False
        
        # Limpiar el código después de usarlo
        self.otp_code = None
        self.otp_created_at = None
        self.save()
        return True
    
    def get_totp_uri(self):
        """Genera URI para QR code con autenticador (Google Authenticator)"""
        if not self.mfa_secret:
            self.mfa_secret = pyotp.random_base32()
            self.save()
        
        totp = pyotp.TOTP(self.mfa_secret)
        return totp.provisioning_uri(name=self.correo, issuer_name='NUAM')
    
    def verify_totp(self, token):
        """Verifica un token TOTP del autenticador"""
        if not self.mfa_secret:
            return False
        
        totp = pyotp.TOTP(self.mfa_secret)
        return totp.verify(token)
    
    def __str__(self):
        return self.correo