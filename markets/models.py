from django.db import models
from website.models import Config
from data.constants import *


class Currency(models.Model):
    name = models.CharField(max_length=128)
    alpha_3 = models.CharField(max_length=3, primary_key=True)



class Commodity(models.Model):
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=32, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    group = models.CharField(max_length=21, choices=enumerate(COMMODITY_GROUPS), null=True, blank=True)



