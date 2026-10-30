from django.db import connection
from django.test import TestCase


class SQLiteSetupTests(TestCase):
    def test_sqlite_is_configured_for_tests(self):
        self.assertEqual(connection.vendor, 'sqlite')

    def test_homepage_loads(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/index.html')

    def test_about_page_loads(self):
        response = self.client.get('/about')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/about.html')

    def test_legacy_listings_url_redirects(self):
        response = self.client.get('/listings.html')

        self.assertRedirects(response, '/listings/')
