from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from .choices import PATH_CHOICES
from country.external_api_providers import CountriesIOProvider as CProvider


class Diplomat(models.Model):
    """Class which represents the Diplomat Object"""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15,
                             validators=[RegexValidator(
                                 regex=settings.PHONE_REGEX)])
    email = models.EmailField(blank=True)
    age = models.IntegerField()
    path = models.CharField(choices=PATH_CHOICES, max_length=255)
    # Relation to Country in the External API RestCountries.eu by ISO 2 Code
    country_iso = models.CharField(choices=CProvider.get_iso2_choices(),
                                   max_length=2,
                                   verbose_name='Country ISO2 Code')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def country(self):
        return CProvider.get_iso2_codes().get(self.country_iso)

    def __str__(self):
        return f'{self.full_name}: {self.get_path_display()}'
