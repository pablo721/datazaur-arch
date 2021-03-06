import pandas as pd
import numpy as np
import requests
import os
import json
from django.conf import settings
import ccxt
import re
from pycoingecko import CoinGeckoAPI
from forex_python.converter import CurrencyRates

from .models import *
from utils.decorators import prep_crypto_display, load_or_save
from utils.formatting import *
from data import constants


CURRENCY = constants.DEFAULT_CURRENCY
API_KEY = os.environ.get("CRYPTOCOMPARE_API_KEY")

def gecko_quote(base, quote):
	gecko = pycoingecko.CoinGeckoAPI()
	coin = CryptoCURRENCY.objects.filter(symbol=base).first().coin_id
	data = gecko.get_coin_by_id(coin)['market_data']
	price = data['current_price'][quote]
	mcap = data['market_cap']
	daily_chg = data['price_change_percentage_24h']
	weekly_chg = data['price_change_percentage_7d']
	monthly_chg = data['price_change_percentage_30d']
	yearly_chg = data['price_change_percentage_1y']
	return coin, price, mcap, daily_chg, weekly_chg, monthly_chg, yearly_chg


def find_quotes(base, quote, exchanges):
	quotes = {}
	ticker = base.upper() + '/' + quote.upper()
	for exchange_id in exchanges:
		exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True})
		markets = pd.DataFrame(exchange.load_markets()).transpose()
		if ticker in markets.index:
			quotes[exchange_id] = exchange.fetch_ticker(ticker)['last']
	return quotes


def get_crypto_value(coin, quote, amount):
	coins = top_coins_by_mcap()

	if CURRENCY != quote:
		rates = CurrencyRates()
		exchange_rate = rates.get_rate(CURRENCY, quote)
	else:
		exchange_rate = 1

	price = coins[coins['Symbol'] == coin]['Price'].iloc[0]
	return amount * price * exchange_rate


def get_portfolio_value(portfolio, CURRENCY):
	value = 0
	currencies = settings.SORTED_CURRENCIES
	for k, v in portfolio.items():
		if k in currencies:
			value += get_CURRENCY_value(k, CURRENCY, v)
		else:
			value += get_crypto_value(k, CURRENCY, v)

	return value


def watchlist_prices(watchlist):
	quote_curr = watchlist.CURRENCY.symbol

	source = watchlist.default_source.name.lower()
	exchange = getattr(ccxt, source)({'enableRateLimit': True})
	coins = watchlist.coins.all()
	rdy_coins = list(filter(lambda x: x.symbol.upper() in exchange.codes, coins))

	tickers = [f'{coin.symbol.upper()}/{quote_curr}' for coin in rdy_coins]

	markets = pd.DataFrame(exchange.load_markets()).transpose()
	ready_tickers = []
	for ticker in tickers:
		if ticker in markets.index:
			ready_tickers.append(ticker)
	# elif ticker.split()

	try:
		prices = exchange.fetch_tickers(tickers)
		print(prices)
		if not prices:
			tickers = []
		return prices

	except Exception as e:
		print(f'error {e}')


def get_coins_info():
	url = f'https://min-api.cryptocompare.com/data/all/coinlist?api_key={API_KEY}'
	data = pd.DataFrame(requests.get(url).json()['Data']).transpose()[['Id', 'Name', 'Symbol', 'CoinName',
																	   'FullName', 'Description', 'Algorithm',
																	   'ProofType', 'TotalCoinsMined',
																	   'CirculatingSupply', 'MaxSupply',
																	   'BlockReward', 'AssetWebsiteUrl',
																	   'IsUsedInDefi', 'IsUsedInNft']]
	return data


def update_coin_prices(currency=constants.DEFAULT_CURRENCY):
	n_new = 0
	n_upd = 0
	url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=100&tsym={currency}&api_key={API_KEY}'
	cols = ['CoinInfo.Name', f'RAW.{currency}.PRICE', f'RAW.{currency}.TOTALVOLUME24H',
		    f'RAW.{currency}.HIGH24HOUR', f'RAW.{currency}.LOW24HOUR',
			f'RAW.{currency}.CHANGE24HOUR']

	df = pd.json_normalize(requests.get(url).json()['Data']).loc[:, cols]
	df.columns = ['base', 'bid', 'daily_vol', 'daily_high', 'daily_low', 'daily_delta']
	df['quote'] = currency
	df['ask'] = 0
	for i, r in df.iterrows():
		if not CryptoFiatTicker.objects.filter(base=r['base'].upper()).filter(quote=currency).exists():
			CryptoFiatTicker.objects.create(**r)
			n_new += 1
		else:
			ticker = CryptoFiatTicker.objects.filter(base=r['base']).filter(quote=currency)[0]
			ticker.__dict__.update(**r)
			ticker.save()
			n_upd += 1
		print(str(**r))
	print(f'Created {n_new} tickers \n ' f'Updated prices of {n_upd} tickers')





@load_or_save('crypto_small.csv', 600)
def coins_by_mcap():

	url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=50&tsym={CURRENCY}&api_key={API_KEY}'
	cols = f'CoinInfo.Name RAW.{CURRENCY}.PRICE RAW.{CURRENCY}.CHANGE24HOUR RAW.{CURRENCY}.CHANGEPCT24HOUR'.split()
	df = pd.json_normalize(requests.get(url).json()['Data'])[cols]
	df.columns = ['Symbol', 'Price', '24h ??', '24h %??']
	return df


@load_or_save('crypto.csv', 1200)
def top_coins_by_mcap():
	url = f'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=100&tsym={CURRENCY}&api_key={API_KEY}'
	cols = f'CoinInfo.Name CoinInfo.FullName CoinInfo.Url RAW.{CURRENCY}.PRICE ' \
		   f'RAW.{CURRENCY}.CHANGEPCTHOUR RAW.{CURRENCY}.CHANGEPCT24HOUR ' \
		   f'RAW.{CURRENCY}.TOTALVOLUME24HTO ' \
		   f'RAW.{CURRENCY}.MKTCAP RAW.{CURRENCY}.SUPPLY RAW.{CURRENCY}.LASTUPDATE'.split()
	df = pd.json_normalize(requests.get(url).json()['Data']).loc[:, cols]
	df.columns = ['Symbol', 'Name', 'Url', 'Price', '1h ??', '24h ??', '24h vol', f'Market cap ({CURRENCY})',
				  'Supply', 'Updated']
	df.dropna(inplace=True)
	df.iloc[:, 3:6] = df.iloc[:, 3:6].astype('float64').round(3)
	df.iloc[:, 6:9] = df.iloc[:, 6:9].astype('int64')

	return prepare_df_display(df)






@load_or_save('exchanges.csv', 86400)
def exchanges_by_vol():
	url = f'https://min-api.cryptocompare.com/data/exchanges/general?api_key={API_KEY}&tsym={CURRENCY}'
	df = pd.DataFrame(requests.get(url).json()['Data']).transpose()[
		['Name', 'Country', 'Grade', 'TOTALVOLUME24H', 'AffiliateURL']]
	df['Name'] = df.apply(lambda x: f"""<a href={x['AffiliateURL']}>{x['Name']}</a>""", axis=1)
	df['24h vol (BTC)'] = df['TOTALVOLUME24H'].apply(lambda x: x['BTC'], True).round(3)
	df[f'24h vol ({CURRENCY})'] = df['TOTALVOLUME24H'].apply(lambda x: '%.3f' % x[CURRENCY], True)
	df = df.drop(['TOTALVOLUME24H', 'AffiliateURL'], axis=1).sort_values(by='24h vol (BTC)',
																		 ascending=False).reset_index(drop=True)
	vol_col = f'Volume ({CURRENCY})'
	df.columns = ['Name', 'Country', 'Grade', vol_col, 'Url']
	df.drop('Url', axis=1, inplace=True)
	df[vol_col] = list(map(lambda x: format(x, ','), df[vol_col]))
	return df


def global_metrics():
	gecko = CoinGeckoAPI()
	return pd.DataFrame(gecko.get_global())


def market_dominance(top_n_coins):
	filename = '~/PycharmProjects/datazaur_web/crypto.csv'
	coins = pd.read_csv(filename, index_col=0).loc[:top_n_coins, f'Market cap ({CURRENCY})']


def prep_market_df(df, n_decimals=3):
	df.columns = ['Symbol', 'Price', '24h ??'] if len(df.columns) == 3 else ['Symbol', 'Price', '24h ??', '24h %??']
	df.iloc[:, 1:] = df.iloc[:, 1:].applymap(lambda x: float(str(x).replace('%', '').replace('+', ''))).round(
		n_decimals).applymap(lambda x: format(x, ','))
	df['24h %??'] = df['24h %??'].apply(lambda x: f'{x}%')
	df.iloc[:, 2:] = df.iloc[:, 2:].applymap(color_cell)
	df.iloc[:, 2] = df.iloc[:, 2].astype(str) + '<br>' + df.iloc[:, 3].astype(str)
	return df.iloc[:, :-1]
