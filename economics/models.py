from django.db import models
from django.core.validators import MaxValueValidator


class Country(models.Model):
    alpha_2 = models.CharField(max_length=2, primary_key=True)
    alpha_3 = models.CharField(max_length=3)
    name = models.CharField(max_length=64, blank=False)
    numeric = models.IntegerField()
    currencies = models.ManyToManyField('markets.Currency', related_name='country_currencies')
    official_name = models.CharField(max_length=128)
    gdp = models.FloatField()
    gdp_ppp = models.FloatField()
    population = models.IntegerField(validators=[MaxValueValidator(30_000_000_000)])



