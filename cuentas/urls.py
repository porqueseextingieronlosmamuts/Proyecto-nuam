from django.urls import path
from . import views
app_name = 'cuentas'

urlpatterns = [
    path('login/', views.inicio_sesion, name='login'),
    path('register/', views.registro, name='registro'),
    path('verificar-mfa/', views.verificar_mfa, name='verificar_mfa'),
    path('habilitar-mfa/', views.habilitar_mfa, name='habilitar_mfa'),
]