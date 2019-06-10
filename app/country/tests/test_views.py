from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

COUNTRY_LIST_URL = reverse('country-list')
COUNTRY_DETAIL_URL = reverse('country-detail', args=['bg'])


def get_country_url_with_filters(filters: dict):
    tokens = [COUNTRY_LIST_URL, '?']
    filters_paired_tokens = list(map(lambda kv: '='.join(kv), filters.items()))
    joined_filters = '&'.join(filters_paired_tokens)
    tokens.append(joined_filters)

    return ''.join(tokens)


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
        response = self.client.get(COUNTRY_DETAIL_URL)

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
        self.assertTemplateUsed(response, 'country_list.html')

    def test_country_detail_GET(self):
        """Test retrieving detail of Country."""
        response = self.client.get(COUNTRY_DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'country_detail.html')

    def test_country_query_filter_by_name(self):
        """Test the filtering by name."""
        url = get_country_url_with_filters({'name': 'Bulgaria'})

        response = self.client.get(url)

        object_list = response.context.get('object_list', None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'country_list.html')
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0]['name'], 'Bulgaria')

    def test_country_query_filter_by_iso(self):
        """Test the filtering by iso."""
        url = get_country_url_with_filters({'iso': 'NL'})

        response = self.client.get(url)

        object_list = response.context.get('object_list', None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'country_list.html')
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0]['name'], 'Netherlands')

    def test_country_query_filter_by_region(self):
        """Test the filtering by region."""

        url = get_country_url_with_filters({'region': 'Polar'})

        response = self.client.get(url)

        object_list = response.context.get('object_list', None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'country_list.html')
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0]['name'], 'Antarctica')

    def test_country_query_filter_by_all_filters(self):
        """Test the filtering by all three filters: 'name', 'iso', 'region'."""
        url = get_country_url_with_filters({'name': 'Bol',
                                            'region': 'Americas',
                                            'iso': 'BO'})

        response = self.client.get(url)

        object_list = response.context.get('object_list', None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'country_list.html')
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0]['name'],
                         'Bolivia (Plurinational State of)')
