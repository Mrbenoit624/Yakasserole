import unittest
from django.test import Client

from django.contrib.auth import views
from .views import profile, public_profile, connect, inscription
from django.contrib.auth.models import User

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.admin = User.objects.create_superuser('admin', '', 'admin1234')

    def test_login(self):
        response = self.client.get('/accounts/login/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__,
                views.LoginView.as_view().__name__)
        print('test login: ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

    def test_profile(self):
        response = self.client.get('/accounts/profile/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__,
                views.LoginView.as_view().__name__)
        print('test profile: ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

    def test_profile_public(self):
        response = self.client.get('/accounts/profile/1/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__,
                views.LoginView.as_view().__name__)
        print('test profil public: ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

    def test_registration(self):
        response = self.client.get('/accounts/register', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, inscription)
        print('test registration: ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

    def test_connect(self):
        response = self.client.get('/accounts/connect', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, connect)
        print('test connect: ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

    def test_payments(self):
        response = self.client.get('/accounts/payments', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__,
                views.LoginView.as_view().__name__)
        print('test payments: ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')

    def test_premium(self):
        response = self.client.get('/accounts/devenir_premium', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__,
                views.LoginView.as_view().__name__)
        print('test premium: ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
    
    def test_profile_admin(self):
        User.objects.create_superuser('admin', '', 'admin1234')
        self.client.login(username='admin', password='admin1234')
        response = self.client.get('/accounts/profile/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, profile)
        print('test admin profil: ' + '\x1b[1;32m' + 'OK' + '\x1b[0m')
