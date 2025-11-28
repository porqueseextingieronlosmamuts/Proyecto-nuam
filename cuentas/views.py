from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UsuarioForm
from .models import Usuario
from django.contrib import messages

# Create your views here.
def inicio_sesion(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']

        usuario = Usuario.objects.filter(correo=correo).first()
        
        if usuario and usuario.check_password(password):
            auth_user = authenticate(request, username=correo, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('dashboard:dashboard')  # Redirige al dashboard después de login
            else:
                messages.error(request, 'Credenciales incorrectas')
        else:
            messages.error(request, 'Correo o contraseña incorrectas')
    return render(request, 'login.html')

def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada con exito')
            return redirect('cuentas:login')
        else: 
            messages.error(request, 'Error al crear la cuenta')
    else:
        form = UsuarioForm()

    return render(request, 'registro.html', {'form': form})
