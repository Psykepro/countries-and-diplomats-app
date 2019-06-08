import requests

from django.conf import settings


def get_detail_url_by_iso(iso):
    return f'{settings.EXTERNAL_COUNTRIES_API_BASE_URL}/alpha/{iso}'


def get_every_iso_2_code_with_country_name():
    response = requests.get(settings.ISO_CODES_API_URL)
    return response.json()


def get_every_iso_2_code():
    response_data = get_every_iso_2_code_with_country_name()
    return [k for k, v in response_data.items()]


def extract_defined_fields_only(cls, passed_fields):
    """This utility method will be used to extract only defined fields
       from the External API."""

    # Skipping ID because it is automatically generated by Django
    defined_fields = [field.attname for field in cls._meta.fields
                      if field.attname != 'id']

    extracted_fields = {k: v for k, v in passed_fields.items()
                        if k in defined_fields}
    return extracted_fields
