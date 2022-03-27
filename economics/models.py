from django.db import models
from django.core.validators import MaxValueValidator


class Country(models.Model):
    name = models.CharField(max_length=64, blank=False)
    alpha_2 = models.CharField(max_length=2, primary_key=True)
    currencies = models.ManyToManyField('markets.Currency',  related_name='currency_country')


