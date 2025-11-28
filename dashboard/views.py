from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Calificacion
from .forms import CalificacionForm
from datetime import datetime

from .forms import CalificacionForm, CargaCalificacionesForm
from .utils import importar_calificaciones_desde_excel

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def intento_logout(request):
    logout(request)
    return redirect('cuentas:login')

@login_required
def agregar_calificacion(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            # Guardar la calificación en la base de datos
            form.save()
            messages.success(request, 'Calificación agregada exitosamente.')
            return redirect('dashboard:buscar_calificaciones')  # Redirigir a la lista de calificaciones (ajustar URL)
        else:
            # Si el formulario no es válido, volver a mostrarlo con los errores
            return render(request, 'agregar_calificacion.html', {'form': form})
    else:
        # Si la solicitud es GET, mostrar el formulario vacío
        form = CalificacionForm()
        return render(request, 'agregar_calificacion.html', {'form': form})

@login_required 
def modificar_calificacion(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)  # Obtener la calificación por su PK
    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()  # Guardar los cambios
            return redirect('dashboard:buscar_calificaciones')  # Redirigir a la lista de calificaciones
    else:
        form = CalificacionForm(instance=calificacion)  # Cargar la calificación en el formulario
    return render(request, 'modificar_calificacion.html', {'form': form, 'calificacion': calificacion})

@login_required
def buscar_calificaciones(request):
    # Obtener los parámetros de búsqueda
    ejercicio = request.GET.get('ejercicio', '')
    mercado = request.GET.get('mercado', '')
    fecha = request.GET.get('fecha', '')
    
    # Filtrar las calificaciones
    calificaciones = Calificacion.objects.all()

    if ejercicio:
        calificaciones = calificaciones.filter(ejercicio=ejercicio)
    if mercado:
        calificaciones = calificaciones.filter(mercado__icontains=mercado)  # Filtrado por texto, 'icontains' es insensible a mayúsculas/minúsculas
    if fecha:
        try:
            fecha = datetime.strptime(fecha, '%d-%m-%Y')  # Convertir la fecha de string a datetime
            calificaciones = calificaciones.filter(fecha=fecha)
        except ValueError:
            pass  # Si la fecha es incorrecta, ignorar el filtro

    return render(request, 'buscar_calificaciones.html', {'calificaciones': calificaciones})

@login_required
def eliminar_calificacion(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)

    if request.method == 'POST':
        calificacion.delete()
        # Después de eliminar, vuelve a la búsqueda de calificaciones
        return redirect('dashboard:buscar_calificaciones')

    # Si es GET, muestra la pantalla de confirmación
    return render(request, 'eliminar_calificacion.html', {
        'calificacion': calificacion,
    })

@login_required
def carga_calificaciones_excel(request):
    if request.method == "POST":
        form = CargaCalificacionesForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.cleaned_data['archivo']

            try:
                importar_calificaciones_desde_excel(archivo)
            except Exception as e:
                messages.error(request, f"Error al procesar el Excel: {e}")
            else:
                messages.success(request, "Calificaciones cargadas correctamente desde Excel.")
                return redirect('dashboard:buscar_calificaciones')
    else:
        form = CargaCalificacionesForm()

    return render(request, 'carga_calificaciones.html', {'form': form})