from data.constants import DEFAULT_CURRENCY
import pandas as pd
import pycountry
import country_currencies
from ipwhois import IPWhois
from .models import Account


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_location(ip):
    return IPWhois(ip).lookup_whois()['asn_country_code']


def get_currency(location):
    currency = country_currencies.get_by_country(location)
    if not currency:
        return DEFAULT_CURRENCY
    else:
        return currency[0]


def setup_account(request):
    ip = get_client_ip(request)
    location = get_location(ip)
    currency = country_currencies.get_by_country(location)[0]
    account = Account.objects.create(user=request.user, currency=currency, signup_ip=ip, signup_location=location)
    Watchlist.objects.create(user=account)
    Portfolio.objects.create(user=account)


