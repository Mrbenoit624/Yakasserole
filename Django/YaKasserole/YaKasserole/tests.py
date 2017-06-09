import unittest
from django.test import Client

from YaKasserole.views import index

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_home(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, index)
