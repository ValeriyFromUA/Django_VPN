from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class MyTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword',
                                                         email='test@example.ua')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')

    def test_home_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_portal_hub_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('portal_hub'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal_hub.html')

    def test_portal_hub_view_unauthenticated(self):
        response = self.client.get(reverse('portal_hub'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={reverse("portal_hub")}')

    def test_portal_view_unauthenticated(self):
        website_path = 'https://stackoverflow.com/questions'
        response = self.client.get(reverse('portal', args=[website_path]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={reverse("portal", args=[website_path])}')
