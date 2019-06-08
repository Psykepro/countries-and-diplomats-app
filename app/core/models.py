from django.db import models

from country.utilities import extract_defined_fields_only


class Country(models.Model):
    """Model representing the Country Object from External API"""
    name = models.CharField(max_length=255)
    alpha2Code = models.CharField(max_length=2, verbose_name='ISO Code')
    capital = models.CharField(max_length=255, verbose_name='Capital City')
    area = models.IntegerField()
    population = models.IntegerField()
    flag = models.ImageField(null=True)

    def __init__(self, *args, **kwargs):
        kwargs = extract_defined_fields_only(self.__class__, kwargs)
        super(Country, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name
