from django import forms
from .models import *


class AddCoin(forms.Form):
    coin = forms.ChoiceField(label='Coin', choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['coin'].choices = [(c.symbol, f'{c.name} ({c.symbol})') for c in Cryptocurrency.objects.all()]
        except Exception as e:
            print(f'error: {e}')


class ChangeCurrency(forms.Form):
    currency = forms.ChoiceField(label='Currency', choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['currency'].choices = [(c.id, c.name) for c in Currency.objects.all()]
        except Exception as e:
            print(f'error: {e}')


class NewWatchlist(forms.Form):
    name = forms.CharField(label='Name', max_length=16)
    type = forms.ChoiceField(label='Type', choices=((1, 'Watchlist'), (2, 'Portfolio')))
    currency = forms.ChoiceField(label='Currency', choices=())
    source = forms.ChoiceField(label='Source', choices=())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].choices = [(c.symbol, c.name) for c in Currency.objects.all()]
        self.fields['source'].choices = [(e.id, e.name) for e in CryptoExchange.objects.all()]



class AddToPortfolio(forms.Form):
    coin = forms.ChoiceField(label='Coin', required=True)
    amount = forms.FloatField(label='Amount', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coin'].choices = [(c.id, c.name) for c in Cryptocurrency.objects.all()]


class SetSource(forms.Form):
    source = forms.ChoiceField(label='Source', choices=())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].choices = [(ex.id, ex.name) for ex in CryptoExchange.objects.all()]



