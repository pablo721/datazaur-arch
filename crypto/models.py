from django.db import models
from markets.models import Market, Asset
from data.constants import *


class CryptoAsset(Asset):
    url = models.CharField(max_length=128)


class Cryptocurrency(CryptoAsset):
    hash_algorithm = models.CharField(max_length=64)
    proof_type = models.CharField(max_length=32)
    total_coins_mined = models.FloatField()
    circ_supply = models.FloatField()
    max_supply = models.FloatField()
    block_reward = models.FloatField()
    used_in_defi = models.BooleanField()
    used_in_nft = models.BooleanField()


class NFT(CryptoAsset):
    floor_price = models.FloatField()
    quote_curr = models.CharField(max_length=16)
    collection = models.ForeignKey('crypto.NFTCollection', on_delete=models.CASCADE)


class NFTCollection(models.Model):
    name = models.CharField(max_length=128)


class CryptoExchange(Market):
    crypto_only = models.BooleanField()
    kyc = models.BooleanField()
    grade = models.CharField(choices=enumerate(CRYPTO_EXCHANGE_GRADES), max_length=3)



