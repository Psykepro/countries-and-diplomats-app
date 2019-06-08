import requests

from django.test import TestCase

from core import models
from country import utilities


class ModelTests(TestCase):

    def test_country_str(self):
        """Test the Country string representation"""
        response = requests.get(utilities.get_country_url_by_iso('bg')).json()
        country = models.Country(**response)

        self.assertEqual(str(country), response['name'])
