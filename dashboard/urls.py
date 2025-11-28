from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logout/', views.intento_logout, name='logout'),
    path('calificaciones/agregar/', views.agregar_calificacion, name='agregar_calificacion'),
    path('calificaciones/<int:pk>/editar', views.modificar_calificacion, name='modificar_calificacion'),
    path('calificaciones/buscar/', views.buscar_calificaciones, name='buscar_calificaciones'),
    path('calificaciones/<int:pk>/eliminar/', views.eliminar_calificacion, name='eliminar_calificacion'),
    path('carga_calificacion/', views.carga_calificaciones_excel, name='carga_masiva'),
]