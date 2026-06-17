from django.contrib import admin
from .models import Gasto, Ingreso

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'monto', 'categoria', 'fecha', 'usuario')
    list_filter = ('categoria', 'fecha', 'usuario')
    search_fields = ('descripcion',)

@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'monto', 'categoria', 'fecha', 'usuario')
    list_filter = ('categoria', 'fecha', 'usuario')
    search_fields = ('descripcion',)
