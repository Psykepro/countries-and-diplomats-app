from django.db import models

from .external_api_providers import (RestCountriesProvider as RProvider,
                                     CountriesIOProvider as CProvider)
from .choices import REGION_CHOICES


class Country(models.Model):
    """Model representing the Country Object from the External API"""
    name = models.CharField(max_length=255)
    alpha2Code = models.CharField(choices=CProvider.get_iso2_choices(),
                                  max_length=2,
                                  verbose_name='ISO Code')
    capital = models.CharField(max_length=255, verbose_name='Capital City')
    area = models.IntegerField()
    population = models.IntegerField()
    flag = models.ImageField(null=True)
    region = models.CharField(choices=REGION_CHOICES,
                              max_length=max([len(x[0]) for x
                                              in REGION_CHOICES]))

    def __init__(self, *args, **kwargs):
        kwargs = RProvider\
            .extract_defined_fields_only(self.__class__, kwargs)
        super(Country, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name
