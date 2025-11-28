from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UsuarioForm
from .models import Usuario
import qrcode
from io import BytesIO
import base64

# Create your views here.
def inicio_sesion(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']

        usuario = Usuario.objects.filter(correo=correo).first()
        
        if usuario and usuario.check_password(password):
            # Si MFA está habilitado, ir a verificación de MFA
            if usuario.mfa_enabled:
                request.session['usuario_id_mfa'] = usuario.id
                
                # Enviar OTP por email
                otp = usuario.generate_otp()
                send_mail(
                    'Código de verificación MFA - NUAM',
                    f'Tu código de verificación es: {otp}\n\nEste código es válido por 10 minutos.',
                    settings.DEFAULT_FROM_EMAIL,
                    [usuario.correo],
                    fail_silently=False,
                )
                
                messages.info(request, 'Se ha enviado un código a tu correo. Por favor verifica.')
                return redirect('cuentas:verificar_mfa')
            
            # Si no tiene MFA, login directo
            auth_user = authenticate(request, username=correo, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('dashboard:dashboard')
            else:
                messages.error(request, 'Credenciales incorrectas')
        else:
            messages.error(request, 'Correo o contraseña incorrectas')
    return render(request, 'login.html')

def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Cuenta creada con éxito. Por favor inicia sesión.')
                return redirect('cuentas:login')
            except Exception as e:
                messages.error(request, f'Error al crear la cuenta: {str(e)}')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UsuarioForm()

    return render(request, 'registro.html', {'form': form})

def verificar_mfa(request):
    """Verifica el código MFA del usuario"""
    usuario_id = request.session.get('usuario_id_mfa')
    
    if not usuario_id:
        return redirect('cuentas:login')
    
    usuario = Usuario.objects.get(id=usuario_id)
    
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        
        if usuario.verify_otp(codigo):
            # OTP correcto, hacer login
            auth_user = authenticate(request, username=usuario.correo, password=request.session.get('password'))
            if auth_user is None:
                # Autenticación directa sin password
                login(request, usuario)
            del request.session['usuario_id_mfa']
            messages.success(request, 'Verificación exitosa')
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Código incorrecto o expirado. Intenta de nuevo.')
    
    return render(request, 'verificar_mfa.html', {'correo': usuario.correo})

def habilitar_mfa(request):
    """Permite al usuario habilitar MFA en su cuenta"""
    usuario = request.user
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'habilitar':
            # Generar URI para QR
            uri = usuario.get_totp_uri()
            
            # Generar QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(uri)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return render(request, 'habilitar_mfa.html', {
                'qr_code': qr_code_base64,
                'secret': usuario.mfa_secret,
                'step': 'verificar'
            })
        
        elif accion == 'confirmar':
            # Verificar que el usuario ingrese el código correcto del autenticador
            codigo = request.POST.get('codigo')
            
            if usuario.verify_totp(codigo):
                usuario.mfa_enabled = True
                usuario.save()
                messages.success(request, 'MFA habilitado correctamente')
                return redirect('dashboard:dashboard')
            else:
                messages.error(request, 'Código incorrecto. Intenta de nuevo.')
        
        elif accion == 'deshabilitar':
            # Deshabilitar MFA
            usuario.mfa_enabled = False
            usuario.mfa_secret = None
            usuario.save()
            messages.success(request, 'MFA deshabilitado')
            return redirect('dashboard:dashboard')
    
    return render(request, 'habilitar_mfa.html', {'mfa_enabled': usuario.mfa_enabled})
