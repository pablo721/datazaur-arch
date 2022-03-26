from django.contrib import admin
from .models import *

admin.site.register(Asset)
admin.site.register(Commodity)
admin.site.register(Currency)
admin.site.register(Market)
admin.site.register(Ticker)
admin.site.register(Watchlist)
admin.site.register(Portfolio)
admin.site.register(PortfolioAmounts)


