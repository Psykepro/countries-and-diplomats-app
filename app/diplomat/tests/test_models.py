from ..models import Diplomat
from django.test import TestCase

from ..choices import PATH_CHOICES


def get_display_val_of_choice_field(choices, val):
    res = [pair[1] for pair in choices if pair[0] == val]
    return res[0] if len(res) > 0 else None


class ModelTests(TestCase):

    def test_diplomat_str(self):
        """Test the Diplomat string representation"""
        payload = {'first_name': 'John',
                   'last_name': 'Doe',
                   'phone': '+359123456789',
                   'email': 'name@domainname.com',
                   'age': '28',
                   'path': 'CO',
                   'country_iso': 'BG'
                   }

        diplomat = Diplomat.objects.create(**payload)

        display_path_val = get_display_val_of_choice_field(PATH_CHOICES,
                                                           payload['path'])
        expected = f"{payload['first_name']} {payload['last_name']}: " \
                   f"{display_path_val}"
        self.assertEqual(str(diplomat), expected)
