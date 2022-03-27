from django.db import models
from data import constants


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    symbol = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    hash_algorithm = models.CharField(max_length=64)
    proof_type = models.CharField(max_length=32)
    total_coins_mined = models.FloatField()
    circ_supply = models.FloatField()
    max_supply = models.FloatField()
    block_reward = models.FloatField()
    used_in_defi = models.BooleanField()
    used_in_nft = models.BooleanField()


class Ticker(models.Model):
    base = models.CharField(max_length=32)
    quote = models.CharField(max_length=32)
    bid = models.FloatField()
    ask = models.FloatField()
    daily_low = models.FloatField()
    daily_high = models.FloatField()
    hourly_delta = models.FloatField()
    daily_delta = models.FloatField()
    weekly_delta = models.FloatField()
    daily_vol = models.FloatField()
    monthly_vol = models.FloatField()



# class NFT(models.Model):
#     name = models.CharField(max_length=64, blank=False, null=False)
#     symbol = models.CharField(max_length=32)
#     floor_price = models.FloatField()
#     quote_curr = models.CharField(max_length=16)
#     collection = models.ForeignKey('crypto.NFTCollection', on_delete=models.CASCADE)
#
#
# class NFTCollection(models.Model):
#     name = models.CharField(max_length=128)
#     symbol = models.CharField(max_length=32)


class CryptoExchange(models.Model):
    name = models.CharField(max_length=128)
    crypto_only = models.BooleanField()
    grade = models.CharField(choices=enumerate(constants.CRYPTO_EXCHANGE_GRADES), max_length=3)
    url = models.CharField(max_length=128)
    countries = models.ManyToManyField('economics.Country')
    currencies = models.ManyToManyField('markets.Currency')
    tickers = models.ManyToManyField('crypto.Cryptocurrency', related_name='market_tickers')
    daily_vol = models.FloatField()
    monthly_vol = models.FloatField()


class Watchlist(models.Model):
    creator = models.ForeignKey('website.Account', related_name='watchlist_creator', on_delete=models.CASCADE)
    followers = models.ManyToManyField('website.Account', related_name='watchlist_followers')
    name = models.CharField(max_length=32, default='Watchlist')
    currency = models.ForeignKey('markets.Currency', on_delete=models.CASCADE, related_name='watchlist_currency')
    watched_coins = models.ManyToManyField('crypto.Cryptocurrency', related_name='watchlist_coins')
    source = models.ForeignKey('crypto.CryptoExchange', on_delete=models.CASCADE, related_name='watchlist_source')


class Portfolio(models.Model):
    owner = models.ForeignKey('website.Account', related_name='portfolio_owner', on_delete=models.CASCADE)
    name = models.CharField(max_length=32, default='Portfolio')
    currency = models.ForeignKey('markets.Currency', on_delete=models.CASCADE, related_name='portfolio_currency')
    portf_coins = models.ManyToManyField(Cryptocurrency, related_name='portfolio_coins')
    source = models.ForeignKey(CryptoExchange, on_delete=models.CASCADE, related_name='portfolio_source')
    amounts = models.ManyToManyField(Cryptocurrency, through='portfolioamounts', through_fields=('portfolio', 'coin'),
                                     related_name='portfolio_amounts')


class PortfolioAmounts(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='portfolioamounts_portfolio')
    coin = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE, related_name='portfolioamounts_coin')
    amount = models.FloatField(default=0)

