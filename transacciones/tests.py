from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from .models import Gasto, Ingreso


class GastoCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    def test_create_gasto(self):
        response = self.client.post('/transacciones/gastos/nuevo/', {
            'descripcion': 'Almuerzo',
            'monto': '15000',
            'categoria': 'alimentacion',
            'fecha': '2026-06-01',
        })
        self.assertRedirects(response, '/transacciones/gastos/')
        self.assertEqual(Gasto.objects.count(), 1)
        g = Gasto.objects.first()
        self.assertEqual(g.descripcion, 'Almuerzo')
        self.assertEqual(float(g.monto), 15000)

    def test_list_gastos(self):
        Gasto.objects.create(
            usuario=self.user, descripcion='Test', monto=100,
            categoria='transporte', fecha=date.today()
        )
        response = self.client.get('/transacciones/gastos/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_edit_gasto(self):
        g = Gasto.objects.create(
            usuario=self.user, descripcion='Original', monto=100,
            categoria='transporte', fecha=date.today()
        )
        response = self.client.post(f'/transacciones/gastos/editar/{g.pk}/', {
            'descripcion': 'Editado',
            'monto': '200',
            'categoria': 'servicios',
            'fecha': '2026-06-01',
        })
        self.assertRedirects(response, '/transacciones/gastos/')
        g.refresh_from_db()
        self.assertEqual(g.descripcion, 'Editado')
        self.assertEqual(float(g.monto), 200)

    def test_delete_gasto(self):
        g = Gasto.objects.create(
            usuario=self.user, descripcion='Borrar', monto=50,
            categoria='otros', fecha=date.today()
        )
        response = self.client.post(f'/transacciones/gastos/eliminar/{g.pk}/')
        self.assertRedirects(response, '/transacciones/gastos/')
        self.assertEqual(Gasto.objects.count(), 0)


class IngresoCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    def test_create_ingreso(self):
        response = self.client.post('/transacciones/ingresos/nuevo/', {
            'descripcion': 'Salario',
            'monto': '1500000',
            'categoria': 'salario',
            'fecha': '2026-06-01',
        })
        self.assertRedirects(response, '/transacciones/ingresos/')
        self.assertEqual(Ingreso.objects.count(), 1)

    def test_list_ingresos(self):
        Ingreso.objects.create(
            usuario=self.user, descripcion='Beca', monto=500000,
            categoria='beca', fecha=date.today()
        )
        response = self.client.get('/transacciones/ingresos/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beca')

    def test_edit_ingreso(self):
        i = Ingreso.objects.create(
            usuario=self.user, descripcion='Viejo', monto=100,
            categoria='freelance', fecha=date.today()
        )
        response = self.client.post(f'/transacciones/ingresos/editar/{i.pk}/', {
            'descripcion': 'Nuevo',
            'monto': '300',
            'categoria': 'salario',
            'fecha': '2026-06-01',
        })
        self.assertRedirects(response, '/transacciones/ingresos/')
        i.refresh_from_db()
        self.assertEqual(i.descripcion, 'Nuevo')

    def test_delete_ingreso(self):
        i = Ingreso.objects.create(
            usuario=self.user, descripcion='Borrar', monto=100,
            categoria='familiar', fecha=date.today()
        )
        response = self.client.post(f'/transacciones/ingresos/eliminar/{i.pk}/')
        self.assertRedirects(response, '/transacciones/ingresos/')
        self.assertEqual(Ingreso.objects.count(), 0)


class ReportExportTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')
        Gasto.objects.create(
            usuario=self.user, descripcion='Gasto1', monto=50000,
            categoria='alimentacion', fecha=date.today()
        )
        Ingreso.objects.create(
            usuario=self.user, descripcion='Ingreso1', monto=100000,
            categoria='salario', fecha=date.today()
        )

    def test_pdf_export(self):
        response = self.client.get('/transacciones/exportar/pdf/', {
            'mes': date.today().month,
            'anio': date.today().year,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('fintrack_', response['Content-Disposition'])

    def test_pdf_export_all_history(self):
        response = self.client.get('/transacciones/exportar/pdf/', {'todo': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_excel_export(self):
        response = self.client.get('/transacciones/exportar/excel/', {
            'mes': date.today().month,
            'anio': date.today().year,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('spreadsheetml', response['Content-Type'])
        self.assertIn('fintrack_', response['Content-Disposition'])

    def test_excel_export_all_history(self):
        response = self.client.get('/transacciones/exportar/excel/', {'todo': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('spreadsheetml', response['Content-Type'])

    def test_reporte_selector_page(self):
        response = self.client.get('/transacciones/reporte/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Exportar PDF')
        self.assertContains(response, 'Exportar Excel')
