from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from transacciones.models import Gasto, Ingreso, CATEGORIAS_GASTO
from datetime import date
import json

@login_required
def dashboard(request):
    hoy = date.today()
    usuario = request.user

    gastos_mes = Gasto.objects.filter(usuario=usuario, fecha__month=hoy.month, fecha__year=hoy.year)
    ingresos_mes = Ingreso.objects.filter(usuario=usuario, fecha__month=hoy.month, fecha__year=hoy.year)

    total_gastos = gastos_mes.aggregate(t=Sum('monto'))['t'] or 0
    total_ingresos = ingresos_mes.aggregate(t=Sum('monto'))['t'] or 0
    balance = float(total_ingresos) - float(total_gastos)

    categorias_labels = []
    categorias_data = []
    for cat_key, cat_label in CATEGORIAS_GASTO:
        total = gastos_mes.filter(categoria=cat_key).aggregate(t=Sum('monto'))['t'] or 0
        if total > 0:
            categorias_labels.append(cat_label)
            categorias_data.append(float(total))

    ultimos_gastos = gastos_mes.order_by('-fecha')[:5]
    ultimos_ingresos = ingresos_mes.order_by('-fecha')[:5]

    return render(request, 'dashboard/dashboard.html', {
        'total_gastos': total_gastos,
        'total_ingresos': total_ingresos,
        'balance': balance,
        'categorias_labels': json.dumps(categorias_labels),
        'categorias_data': json.dumps(categorias_data),
        'ultimos_gastos': ultimos_gastos,
        'ultimos_ingresos': ultimos_ingresos,
        'mes': hoy.strftime('%B %Y'),
    })