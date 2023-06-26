#root/home/tests/test_views.py
import unittest
from unittest.mock import MagicMock
from django.test import RequestFactory
from django.contrib.auth.models import User
from accounts.models import entrepreneur
from home.views import home, profile, search

class TestHomeViews(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.ent = entrepreneur.objects.create(user=self.user)

    def tearDown(self):
        self.user.delete()
        self.ent.delete()

    def test_home(self):
        request = self.factory.get('/home/')
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_profile_owner(self):
        request = self.factory.get('/profile/', {'id': 'testuser'})
        request.user = self.user
        response = profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context_data['is_owner'])

    def test_profile_not_owner(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        request = self.factory.get('/profile/', {'id': 'otheruser'})
        request.user = self.user
        response = profile(request)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context_data['is_owner'])
        other_user.delete()

    def test_search_post(self):
        request = self.factory.post('/search/', {'keyword': 'test'})
        request.user = self.user
        response = search(request)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.context_data['result_available'], 0)

    def test_search_get(self):
        request = self.factory.get('/search/')
        request.user = self.user
        response = search(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['result_available'], -1)

if __name__ == '__main__':
    unittest.main()