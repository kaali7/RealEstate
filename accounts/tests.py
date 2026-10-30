from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountTests(TestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'Demo',
            'last_name': 'User',
            'username': 'demo',
            'email': 'demo@example.com',
            'password': 'Demo@12345',
            'password2': 'Demo@12345',
        }

    def test_registration_creates_user_and_redirects_to_login(self):
        response = self.client.post(reverse('register'), self.user_data)

        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='demo').exists())

    def test_registration_rejects_mismatched_passwords(self):
        data = dict(self.user_data, password2='Different@12345')

        response = self.client.post(reverse('register'), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='demo').exists())
        self.assertContains(response, 'Passwords do not match')

    def test_login_redirects_to_dashboard(self):
        User.objects.create_user(
            username='demo',
            password='Demo@12345',
        )

        response = self.client.post(
            reverse('login'),
            {'username': 'demo', 'password': 'Demo@12345'},
        )

        self.assertRedirects(response, reverse('dashboard'))

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))

        self.assertRedirects(
            response,
            '%s?next=%s' % (reverse('login'), reverse('dashboard')),
        )
