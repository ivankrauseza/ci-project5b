from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class HomePageTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))  # Assuming 'home' is the name of your homepage URL
        self.assertEqual(response.status_code, 200)
