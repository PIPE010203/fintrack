from django.db import models
from django.contrib.auth.models import User

CATEGORIAS_GASTO = [
    ('alimentacion', 'Alimentación'),
    ('transporte', 'Transporte'),
    ('universidad', 'Universidad'),
    ('entretenimiento', 'Entretenimiento'),
    ('servicios', 'Servicios'),
    ('otros', 'Otros'),
]

CATEGORIAS_INGRESO = [
    ('salario', 'Salario'),
    ('beca', 'Beca'),
    ('freelance', 'Trabajo Freelance'),
    ('familiar', 'Ayuda Familiar'),
    ('otros', 'Otros'),
]

class Gasto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_GASTO)
    fecha = models.DateField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - ${self.monto}"

    class Meta:
        ordering = ['-fecha']

class Ingreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_INGRESO)
    fecha = models.DateField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - ${self.monto}"

    class Meta:
        ordering = ['-fecha']