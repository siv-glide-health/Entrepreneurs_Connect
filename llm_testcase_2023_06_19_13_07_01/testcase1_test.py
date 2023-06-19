# Test case file: root/accounts/tests.py
import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import entrepreneur

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.ent = entrepreneur.objects.create(user=self.user, city='Test City', industry='Test Industry', intro='Test Intro', state='Test State', country='Test Country', about='Test About')

    def test_register(self):
        response = self.client.post('/accounts/register', {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test2@example.com',
            'username': 'testuser2',
            'password1': 'testpassword2',
            'password2': 'testpassword2'
        })
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        response = self.client.post('/accounts/login', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)

    def test_edit_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/accounts/edit_profile', {
            'city': 'New Test City',
            'industry': 'New Test Industry',
            'intro': 'New Test Intro',
            'state': 'New Test State',
            'country': 'New Test Country',
            'about': 'New Test About'
        })
        self.assertEqual(response.status_code, 302)

    def test_view_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/accounts/view_profile')
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/accounts/logout')
        self.assertEqual(response.status_code, 302)