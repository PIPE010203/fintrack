from django.db import models
from django.contrib.auth.models import User
from transacciones.models import CATEGORIAS_GASTO

class Presupuesto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_GASTO)
    limite = models.DecimalField(max_digits=12, decimal_places=2)
    mes = models.IntegerField()
    anio = models.IntegerField()

    class Meta:
        unique_together = ('usuario', 'categoria', 'mes', 'anio')

    def __str__(self):
        return f"{self.categoria} — ${self.limite}"