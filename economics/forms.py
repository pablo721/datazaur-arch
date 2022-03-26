from django import forms


class FindTicker(forms.Form):
    ticker = forms.CharField(max_length=8)


