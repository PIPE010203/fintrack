import json
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from transacciones.models import Gasto, Ingreso


class ChatbotTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')

    def test_chat_page_renders(self):
        response = self.client.get('/chatbot/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Asistente Financiero IA')

    def test_send_message_without_api_key_returns_error(self):
        response = self.client.post(
            '/chatbot/enviar/',
            json.dumps({'mensaje': 'Hola'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('respuesta', data)

    def test_chat_includes_financial_context(self):
        Gasto.objects.create(
            usuario=self.user, descripcion='Test', monto=50000,
            categoria='alimentacion', fecha=date.today()
        )
        response = self.client.post(
            '/chatbot/enviar/',
            json.dumps({'mensaje': '¿Cuánto gasté?'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
