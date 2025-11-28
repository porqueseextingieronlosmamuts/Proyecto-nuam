from django.urls import path
from . import views
app_name = 'cuentas'

urlpatterns = [
    path('login/', views.inicio_sesion, name='login'),
    path('register/', views.registro, name='registro'),
]