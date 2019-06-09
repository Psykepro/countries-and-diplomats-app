import requests

from django.test import TestCase

from ..models import Country
from ..utilities import RestCountriesUtilities as RUtility


class ModelTests(TestCase):

    def test_country_str(self):
        """Test the Country string representation"""
        response = requests.get(RUtility.get_country_url_by_iso('bg')).json()
        country = Country(**response)

        self.assertEqual(str(country), response['name'])
