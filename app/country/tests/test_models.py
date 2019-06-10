import requests

from django.test import TestCase

from ..models import Country
from ..external_api_providers import RestCountriesProvider as RProvider


class ModelTests(TestCase):

    def test_country_str(self):
        """Test the Country string representation"""
        response = requests.get(RProvider.get_country_url_by_iso('bg')).json()
        country = Country(**response)

        self.assertEqual(str(country), response['name'])
