from django.db import models
from website.models import Config
from data.constants import *


class Asset(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    symbol = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    asset_class = models.CharField(choices=enumerate(ASSET_CLASSES), max_length=32)
    tags = models.ManyToManyField('website.Tag')


class Currency(Asset):
    alpha_3 = models.CharField(max_length=3, blank=False, null=False, primary_key=True)
    numeric = models.CharField(max_length=6)
    issuer = models.OneToOneField('economics.Country', on_delete=models.CASCADE, related_name='currency_issuer')


class Ticker(models.Model):
    base = models.ForeignKey('markets.Asset', on_delete=models.CASCADE, related_name='quote_base')
    quote = models.ForeignKey('markets.Asset', on_delete=models.CASCADE, related_name='quote_quote')
    market = models.ForeignKey('markets.Market', on_delete=models.CASCADE)
    bid = models.FloatField()
    ask = models.FloatField()
    daily_low = models.FloatField()
    daily_high = models.FloatField()
    hourly_delta = models.FloatField()
    daily_delta = models.FloatField()
    weekly_delta = models.FloatField()
    daily_vol = models.FloatField()
    monthly_vol = models.FloatField()


class Market(models.Model):
    name = models.CharField(max_length=82)
    symbol = models.CharField(max_length=16)
    url = models.CharField(max_length=128, default='')
    countries = models.ManyToManyField('economics.Country')
    currencies = models.ManyToManyField('markets.Currency')
    daily_vol = models.FloatField()
    monthly_vol = models.FloatField()
    tickers = models.ManyToManyField('markets.Ticker', related_name='market_tickers')


class Commodity(Asset):
    group = models.CharField(max_length=21, choices=enumerate(COMMODITY_GROUPS))


class Watchlist(models.Model):
    creator = models.ForeignKey('website.Account', related_name='watchlist_creator', on_delete=models.CASCADE)
    followers = models.ManyToManyField('website.Account', related_name='watchlist_followers')
    name = models.CharField(max_length=32, default='watchlist')
    currency = models.ForeignKey('markets.Currency', on_delete=models.CASCADE, related_name='watchlist_currency')
    assets = models.ManyToManyField('markets.Asset', related_name='watchlist_assets')
    source = models.ForeignKey('crypto.CryptoExchange', on_delete=models.CASCADE)


class Portfolio(Watchlist):
    amounts = models.ManyToManyField('markets.Asset', through='portfolioamounts', through_fields=('portfolio', 'asset'))


class PortfolioAmounts(models.Model):
    portfolio = models.ForeignKey('markets.Portfolio', on_delete=models.CASCADE, related_name='portfolioamounts_portfolio')
    asset = models.ForeignKey('markets.Asset', on_delete=models.CASCADE, related_name='portfolioamounts_asset')
    amount = models.FloatField(default=0)
