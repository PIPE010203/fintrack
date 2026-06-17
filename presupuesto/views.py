import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

logger = logging.getLogger(__name__)
from .models import Presupuesto
from .forms import PresupuestoForm
from .utils import calcular_progreso
from datetime import date

@login_required
def lista_presupuestos(request):
    hoy = date.today()
    presupuestos = Presupuesto.objects.filter(usuario=request.user, mes=hoy.month, anio=hoy.year)
    data = []
    for p in presupuestos:
        progreso = calcular_progreso(request.user, p)
        data.append({
            'presupuesto': p,
            'gastado': progreso['gastado'],
            'porcentaje': progreso['porcentaje'],
            'alerta': progreso['alerta'],
        })
    return render(request, 'presupuesto/lista.html', {'data': data})

@login_required
def nuevo_presupuesto(request):
    form = PresupuestoForm(request.POST or None)
    if form.is_valid():
        p = form.save(commit=False)
        p.usuario = request.user
        p.save()
        messages.success(request, 'Presupuesto creado.')
        return redirect('presupuesto')
    return render(request, 'presupuesto/form.html', {'form': form})

@login_required
def eliminar_presupuesto(request, pk):
    p = get_object_or_404(Presupuesto, pk=pk, usuario=request.user)
    if request.method == 'POST':
        p.delete()
        messages.success(request, 'Presupuesto eliminado.')
        return redirect('presupuesto')
    return render(request, 'transacciones/confirmar_eliminar.html', {'objeto': p, 'tipo': 'presupuesto'})