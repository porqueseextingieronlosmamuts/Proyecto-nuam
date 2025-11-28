from django.db import models

# Create your models here.
class Calificacion(models.Model):

    ejercicio = models.IntegerField()
    mercado = models.CharField(max_length=3)
    instrumento = models.CharField(max_length=50)
    fecha = models.DateField()
    secuencia = models.BigIntegerField()
    numero_dividendo = models.BigIntegerField()

    # Tipo sociedad (una letra, A o C)
    TIPO_SOCIEDAD_CHOICES = [
        ('A', 'Abierta'),
        ('C', 'Cerrada'),
    ]
    tipo_sociedad = models.CharField(max_length=1, choices=TIPO_SOCIEDAD_CHOICES)
    valor_historico = models.DecimalField(max_digits=10, decimal_places=2)

    # Factores (todos son números con 8 decimales)
    factor_8 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_9 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_10 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_11 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_12 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_13 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_14 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_15 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_16 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_17 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_18 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_19 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_20 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_21 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_22 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_23 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_24 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_25 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_26 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_27 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_28 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_29 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_30 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_31 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_32 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_33 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_34 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_35 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_36 = models.DecimalField(max_digits=9, decimal_places=8)
    factor_37 = models.DecimalField(max_digits=9, decimal_places=8)