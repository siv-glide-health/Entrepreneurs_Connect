# Test case file: root/home/tests.py
import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from accounts.models import entrepreneur

class HomeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.ent = entrepreneur.objects.create(user=self.user, about="Test entrepreneur", intro="Test intro", industry="Test industry", city="Test city", state="Test state", country="Test country")

    def test_home(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test entrepreneur')

    def test_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/profile/', {'id': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test entrepreneur')
        self.assertContains(response, 'Test intro')
        self.assertContains(response, 'Test industry')
        self.assertContains(response, 'Test city')
        self.assertContains(response, 'Test state')
        self.assertContains(response, 'Test country')

    def test_search(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'result_available')

        response = self.client.post('/search/', {'keyword': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'result_available')
        self.assertContains(response, 'Test entrepreneur')
        self.assertContains(response, 'Test intro')
        self.assertContains(response, 'Test industry')
        self.assertContains(response, 'Test city')
        self.assertContains(response, 'Test state')
        self.assertContains(response, 'Test country')