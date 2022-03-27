from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='user_account')
    currency_code = models.CharField(max_length=3)
    signup_location = models.CharField(max_length=64)
    signup_ip = models.CharField(max_length=45)
    friends = models.ManyToManyField('self')
    exchanges = models.ManyToManyField('crypto.CryptoExchange')
    watchlists = models.ManyToManyField('crypto.Watchlist')

    def __str__(self):
        return self.user.username


class Config(models.Model):
    key = models.CharField(max_length=64, unique=True, null=False, blank=False)
    value = models.CharField(max_length=256)


class Tag(models.Model):
    tag = models.CharField(max_length=32)

