#root/accounts/tests/test_views.py
import unittest
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User, auth
from accounts.models import entrepreneur
from accounts.views import register, login, edit_profile, view_profile, logout
from django.core.files.uploadedfile import SimpleUploadedFile

class TestViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.ent = entrepreneur.objects.create(user=self.user, intro='Test intro', industry='Test industry', city='Test city', state='Test state', country='Test country', about='Test about')

    def test_register(self):
        request = self.factory.post('/accounts/register', {'first_name': 'Test', 'last_name': 'User', 'email': 'test2@example.com', 'username': 'testuser2', 'password1': 'testpassword', 'password2': 'testpassword'})
        request.user = self.user
        response = register(request)
        self.assertEqual(response.status_code, 302)

        request = self.factory.post('/accounts/register', {'first_name': 'Test', 'last_name': 'User', 'email': 'test@example.com', 'username': 'testuser2', 'password1': 'testpassword', 'password2': 'testpassword'})
        request.user = self.user
        response = register(request)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        request = self.factory.post('/accounts/login', {'username': 'testuser', 'password': 'testpassword'})
        request.user = self.user
        response = login(request)
        self.assertEqual(response.status_code, 302)

        request = self.factory.post('/accounts/login', {'username': 'wronguser', 'password': 'testpassword'})
        request.user = self.user
        response = login(request)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile(self):
        request = self.factory.get('/accounts/edit_profile')
        request.user = self.user
        response = edit_profile(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('/accounts/edit_profile', {'city': 'New city', 'industry': 'New industry', 'intro': 'New intro', 'state': 'New state', 'country': 'New country', 'about': 'New about'})
        request.user = self.user
        response = edit_profile(request)
        self.assertEqual(response.status_code, 302)

    def test_view_profile(self):
        request = self.factory.get('/accounts/view_profile')
        request.user = self.user
        response = view_profile(request)
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        request = self.factory.get('/accounts/logout')
        request.user = self.user
        response = logout(request)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        self.user.delete()
        self.ent.delete()