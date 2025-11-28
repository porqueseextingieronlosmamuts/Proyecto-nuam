from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.
class Usuario(AbstractBaseUser, models.Model):

    nombre =  models.CharField(max_length = 100)
    correo = models.EmailField(unique = True)
    password = models.CharField(max_length= 250)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'correo'

    objects = UserManager()