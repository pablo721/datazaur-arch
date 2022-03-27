from django.db import models
from website.models import Config
from data.constants import *


class Currency(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    symbol = models.CharField(max_length=32)
    alpha_3 = models.CharField(max_length=3, blank=False, null=False, primary_key=True)
    numeric = models.CharField(max_length=6)
    issuer = models.ForeignKey('economics.Country', on_delete=models.CASCADE, related_name='currency_issuer')


class Commodity(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    symbol = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    group = models.CharField(max_length=21, choices=enumerate(COMMODITY_GROUPS))



