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

    def test_play_trailer(self):
        response = self.client.get('/focus/157336/') # Hardcode videoId for movie 'Interstellar'
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get('/search/?search=interstellar') # hardcode search item
        self.assertEqual(response.status_code, 200)