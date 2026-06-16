from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Presupuesto
from .forms import PresupuestoForm
from transacciones.models import Gasto
from datetime import date

@login_required
def lista_presupuestos(request):
    hoy = date.today()
    presupuestos = Presupuesto.objects.filter(usuario=request.user, mes=hoy.month, anio=hoy.year)
    data = []
    for p in presupuestos:
        gastado = Gasto.objects.filter(
            usuario=request.user,
            categoria=p.categoria,
            fecha__month=p.mes,
            fecha__year=p.anio
        ).aggregate(total=Sum('monto'))['total'] or 0
        porcentaje = min(int((float(gastado) / float(p.limite)) * 100), 100)
        alerta = porcentaje >= 80
        data.append({
            'presupuesto': p,
            'gastado': gastado,
            'porcentaje': porcentaje,
            'alerta': alerta,
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