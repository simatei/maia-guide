from django.test import TestCase

class TestUrls(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_movies(self):
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, 200)

    def test_shows(self):
        response = self.client.get('/shows/')
        self.assertEqual(response.status_code, 200)