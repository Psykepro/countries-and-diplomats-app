from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

COUNTRY_LIST_URL = reverse('country-list')
COUNTRY_DETAIL_URL = reverse('country-detail', args=['bg'])


class PublicCountryViewsTests(TestCase):
    """Tests for publicly accessed Country's Views."""
    def setUp(self):
        self.client = Client()

    def test_country_list_redirects_unauthenticated(self):
        """Test that country list view redirects unauthenticated users."""
        response = self.client.get(COUNTRY_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_country_detail_redirects_unauthenticated(self):
        """Test that country detail view redirects unauthenticated users."""
        response = self.client.get(reverse('country-detail', args=['bg']))

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class PrivateCountryViewsTests(TestCase):
    """Tests for views which are retrieved by authenticated user."""
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            'test@somedomain.com',
            'testpass1'
        )
        self.client.force_login(self.user)

    def test_country_list_GET(self):
        """Test retrieving list of Countries."""
        response = self.client.get(COUNTRY_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'country/country_list.html')

    def test_country_detail_GET(self):
        """Test retrieving detail of Country."""
        response = self.client.get(reverse('country-detail', args=['bg']))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'country/country_detail.html')
