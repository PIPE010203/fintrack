from django.db import migrations
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from datetime import timedelta


def seed_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Gasto = apps.get_model('transacciones', 'Gasto')
    Ingreso = apps.get_model('transacciones', 'Ingreso')
    Presupuesto = apps.get_model('presupuesto', 'Presupuesto')

    user, _ = User.objects.get_or_create(
        username='demo',
        defaults={
            'email': 'demo@fintrack.app',
            'is_staff': True,
            'password': make_password('demo123'),
        },
    )

    today = timezone.now().date()

    # --- INGRESOS (6 ingresos across 30 days) ---
    ingresos_data = [
        (1, 'Salario medio tiempo', 1200000, 'salario'),
        (5, 'Beca universitaria', 500000, 'beca'),
        (10, 'Trabajo freelance', 350000, 'freelance'),
        (15, 'Ayuda familiar', 200000, 'familiar'),
        (20, 'Trabajo freelance', 280000, 'freelance'),
        (25, 'Salario medio tiempo', 1200000, 'salario'),
    ]
    for dias_atras, desc, monto, cat in ingresos_data:
        Ingreso.objects.create(
            usuario=user,
            descripcion=desc,
            monto=monto,
            categoria=cat,
            fecha=today - timedelta(days=30 - dias_atras),
        )

    # --- GASTOS (30+ entries across 30 days) ---
    gastos_data = [
        # (days_ago, description, amount, category)
        (1,  'Almuerzo restaurante', 18000, 'alimentacion'),
        (1,  'Pasaje bus', 5500, 'transporte'),
        (2,  'Mercado semanal', 85000, 'alimentacion'),
        (3,  'Fotocopias apuntes', 12000, 'universidad'),
        (4,  'Almuerzo U', 15000, 'alimentacion'),
        (4,  'Taxi app', 12000, 'transporte'),
        (5,  'Cine con amigos', 35000, 'entretenimiento'),
        (6,  'Desayuno cafe', 8000, 'alimentacion'),
        (7,  'Recarga TransMilenio', 10000, 'transporte'),
        (8,  'Almuerzo corrientazo', 14000, 'alimentacion'),
        (9,  'Cuenta servicios publicos', 95000, 'servicios'),
        (10, 'Domicilio pizza', 28000, 'alimentacion'),
        (10, 'Bus interurbano', 15000, 'transporte'),
        (11, 'Almuerzo U', 16000, 'alimentacion'),
        (12, 'Plan celular prepago', 25000, 'servicios'),
        (13, 'Mecato tienda', 7000, 'alimentacion'),
        (14, 'Pasaje bus', 5500, 'transporte'),
        (15, 'Salida a comer', 42000, 'entretenimiento'),
        (16, 'Almuerzo corrientazo', 13000, 'alimentacion'),
        (17, 'Lapices y cuadernos', 18500, 'universidad'),
        (18, 'Cena rapida', 22000, 'alimentacion'),
        (19, 'Gasolina (domino)', 30000, 'transporte'),
        (20, 'Mercado semanal', 92000, 'alimentacion'),
        (21, 'Streaming mensual', 15000, 'entretenimiento'),
        (22, 'Almuerzo U', 15000, 'alimentacion'),
        (23, 'Fotocopias', 8000, 'universidad'),
        (24, 'Pasaje bus', 5500, 'transporte'),
        (25, 'Pan y cafe', 6000, 'alimentacion'),
        (26, 'Cuenta internet', 72000, 'servicios'),
        (27, 'Cena familiar', 55000, 'alimentacion'),
        (28, 'Almuerzo restaurante', 20000, 'alimentacion'),
        (29, 'Bus urbano', 5500, 'transporte'),
        (30, 'Compra ropa', 65000, 'otros'),
        (30, 'Cine', 25000, 'entretenimiento'),
    ]
    for dias_atras, desc, monto, cat in gastos_data:
        Gasto.objects.create(
            usuario=user,
            descripcion=desc,
            monto=monto,
            categoria=cat,
            fecha=today - timedelta(days=30 - dias_atras),
        )

    # --- PRESUPUESTOS (monthly budgets) ---
    presupuestos_data = [
        ('alimentacion', 800000),
        ('transporte', 200000),
        ('universidad', 150000),
        ('entretenimiento', 150000),
        ('servicios', 250000),
    ]
    for cat, limite in presupuestos_data:
        Presupuesto.objects.create(
            usuario=user,
            categoria=cat,
            limite=limite,
            mes=today.month,
            anio=today.year,
        )


def unseed_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Gasto = apps.get_model('transacciones', 'Gasto')
    Ingreso = apps.get_model('transacciones', 'Ingreso')
    Presupuesto = apps.get_model('presupuesto', 'Presupuesto')

    try:
        user = User.objects.get(username='demo')
        Gasto.objects.filter(usuario=user).delete()
        Ingreso.objects.filter(usuario=user).delete()
        Presupuesto.objects.filter(usuario=user).delete()
        user.delete()
    except User.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('transacciones', '0001_initial'),
        ('presupuesto', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
