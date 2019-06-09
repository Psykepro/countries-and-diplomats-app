from django.db import models

from .utilities import (RestCountriesUtilities as RUtility,
                        CountriesIOUtilities as CUtility)


class Country(models.Model):
    """Model representing the Country Object from the External API"""
    name = models.CharField(max_length=255)
    alpha2Code = models.CharField(choices=CUtility.get_iso2_codes(),
                                  max_length=2,
                                  verbose_name='ISO Code')
    capital = models.CharField(max_length=255, verbose_name='Capital City')
    area = models.IntegerField()
    population = models.IntegerField()
    flag = models.ImageField(null=True)
    region = models.CharField(choices=RUtility.REGION_CHOICES,
                              max_length=max([len(x[0]) for x
                                              in RUtility.REGION_CHOICES]))

    def __init__(self, *args, **kwargs):
        kwargs = RUtility\
            .extract_defined_fields_only(self.__class__, kwargs)
        super(Country, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name
