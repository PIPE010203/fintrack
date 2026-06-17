from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from .models import Presupuesto
from transacciones.models import Gasto


class PresupuestoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    def test_create_presupuesto(self):
        response = self.client.post('/presupuesto/nuevo/', {
            'categoria': 'alimentacion',
            'limite': '500000',
            'mes': 6,
            'anio': 2026,
        })
        self.assertRedirects(response, '/presupuesto/')
        self.assertEqual(Presupuesto.objects.count(), 1)

    def test_unique_constraint(self):
        Presupuesto.objects.create(
            usuario=self.user, categoria='transporte',
            limite=200000, mes=6, anio=2026
        )
        with self.assertRaises(Exception):
            Presupuesto.objects.create(
                usuario=self.user, categoria='transporte',
                limite=300000, mes=6, anio=2026
            )

    def test_delete_presupuesto(self):
        p = Presupuesto.objects.create(
            usuario=self.user, categoria='servicios',
            limite=100000, mes=6, anio=2026
        )
        response = self.client.post(f'/presupuesto/eliminar/{p.pk}/')
        self.assertRedirects(response, '/presupuesto/')
        self.assertEqual(Presupuesto.objects.count(), 0)

    def test_budget_list_shows_alert_when_limit_reached(self):
        Presupuesto.objects.create(
            usuario=self.user, categoria='alimentacion',
            limite=100000, mes=date.today().month, anio=date.today().year
        )
        Gasto.objects.create(
            usuario=self.user, descripcion='Gasto alto', monto=120000,
            categoria='alimentacion', fecha=date.today()
        )
        response = self.client.get('/presupuesto/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ya alcanzaste el límite de tu presupuesto')

    def test_budget_list_no_alert_when_below_limit(self):
        Presupuesto.objects.create(
            usuario=self.user, categoria='transporte',
            limite=100000, mes=date.today().month, anio=date.today().year
        )
        Gasto.objects.create(
            usuario=self.user, descripcion='Gasto bajo', monto=99900,
            categoria='transporte', fecha=date.today()
        )
        response = self.client.get('/presupuesto/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Ya alcanzaste')
