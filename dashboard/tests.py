from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from transacciones.models import Gasto, Ingreso


class DashboardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    def test_dashboard_aggregates_monthly_totals(self):
        Gasto.objects.create(
            usuario=self.user, descripcion='Gasto1', monto=50000,
            categoria='alimentacion', fecha=date.today()
        )
        Gasto.objects.create(
            usuario=self.user, descripcion='Gasto2', monto=30000,
            categoria='transporte', fecha=date.today()
        )
        Ingreso.objects.create(
            usuario=self.user, descripcion='Ingreso1', monto=200000,
            categoria='salario', fecha=date.today()
        )
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '80000')   # 50000 + 30000
        self.assertContains(response, '200000')  # ingreso
        self.assertContains(response, '120000')  # balance

    def test_dashboard_only_shows_current_month(self):
        Gasto.objects.create(
            usuario=self.user, descripcion='Gasto pasado', monto=99999,
            categoria='otros', fecha=date(2020, 1, 1)
        )
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '99,999')

    def test_dashboard_shows_chart_data(self):
        Gasto.objects.create(
            usuario=self.user, descripcion='Comida', monto=50000,
            categoria='alimentacion', fecha=date.today()
        )
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alimentaci')
