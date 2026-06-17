from django.db.models import Sum
from transacciones.models import Gasto


def calcular_progreso(usuario, presupuesto):
    gastado = Gasto.objects.filter(
        usuario=usuario,
        categoria=presupuesto.categoria,
        fecha__month=presupuesto.mes,
        fecha__year=presupuesto.anio
    ).aggregate(total=Sum('monto'))['total'] or 0

    exceso = max(0, float(gastado) - float(presupuesto.limite))
    porcentaje = int((float(gastado) / float(presupuesto.limite)) * 100)

    return {
        'gastado': gastado,
        'porcentaje': min(porcentaje, 100),
        'exceso': exceso,
        'alerta': porcentaje >= 100,
    }
