from django.contrib import admin
from .models import *

admin.site.register(CryptoAsset)
admin.site.register(Cryptocurrency)
admin.site.register(CryptoExchange)
admin.site.register(NFT)
admin.site.register(NFTCollection)

