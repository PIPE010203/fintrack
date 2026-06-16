from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthFlowTest(TestCase):

    def test_user_registration(self):
        response = self.client.post('/usuarios/registro/', {
            'username': 'testuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertRedirects(response, '/dashboard/')
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_and_logout_flow(self):
        User.objects.create_user(username='testuser', password='ComplexPass123!')
        login = self.client.post('/usuarios/login/', {
            'username': 'testuser',
            'password': 'ComplexPass123!',
        })
        self.assertRedirects(login, '/dashboard/')
        logout = self.client.get('/usuarios/logout/')
        self.assertRedirects(logout, '/usuarios/login/')

    def test_login_with_invalid_credentials(self):
        response = self.client.post('/usuarios/login/', {
            'username': 'nobody',
            'password': 'wrong',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'incorrectos')

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/usuarios/login/?next=/dashboard/')
