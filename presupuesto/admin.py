from django.contrib import admin
from .models import Presupuesto

@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'limite', 'mes', 'anio', 'usuario')
    list_filter = ('categoria', 'mes', 'anio', 'usuario')
