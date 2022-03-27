import pandas as pd
import pycountry
import country_currencies
import ccxt
from pycoingecko import CoinGeckoAPI
import yaml
import json
import re
from django.contrib.auth.models import User
from markets.models import *
from website.models import *
from crypto.models import *
from economics.models import *
from data.constants import *
from crypto.crypto_src import get_coins_info


def load_config(filepath='config.yaml'):
	ext = filepath.split('.')[-1].lower()
	with open(filepath, 'r') as cfg:
		if ext == 'json':
			cfg_data = json.load(cfg.read())
		elif ext in ['yaml', 'yml']:
			cfg_data = yaml.safe_load(cfg)
		else:
			return 'Wrong file type. \n ' \
				   'Need a json/yaml/yml config file.'

	n_upd = 0
	n = Config.objects.all().count()
	for k, v in cfg_data.items():
		if Config.objects.filter(key=k).exists():
			Config.objects.get(key=k).update(value=v)
			n_upd += 1
		else:
			Config.objects.create(key=k, value=v)
	print(f'Added {Config.objects.all().count() - n} parameters to database. \n'
		  f'Updated {n_upd} parameters.')


def setup_all():
	try:
		load_config()
		print('Config loaded.')
		load_countries()
		load_currencies()
		map_currencies_to_countries()

		load_cryptocomp_coins()
		load_gecko_coins()
		load_crypto_exchanges()

		print(f'All imports complete.')
	except Exception as e:
		print(f'Error: {e}')


def load_cryptocomp_coins():
	n = Cryptocurrency.objects.all().count()
	coins = get_coins_info().loc[:, ['Symbol', 'CoinName', 'Description', 'Algorithm', 'ProofType', 'TotalCoinsMined',
									 'CirculatingSupply', 'MaxSupply', 'BlockReward', 'AssetWebsiteUrl',
									 'IsUsedInDefi', 'IsUsedInNft']]
	coins.columns = ['symbol', 'name', 'description', 'hash_algorithm', 'proof_type', 'total_coins_mined',
					 'circ_supply', 'max_supply', 'block_reward', 'url', 'used_in_defi', 'used_in_nft']
	coins['description'] = coins['description'].apply(lambda x: x[:255])
	for i, row in coins.iterrows():
		if not Cryptocurrency.objects.filter(symbol=row['symbol']).exists():
			Cryptocurrency.objects.create(**dict(row))
	print(f'Loaded {Cryptocurrency.objects.all().count() - n} cryptocurrencies from Cryptocompare.')


def load_gecko_coins():
	n = Cryptocurrency.objects.all().count()
	gecko = CoinGeckoAPI()
	coins = pd.DataFrame(columns=['id', 'symbol', 'name'], data=gecko.get_coins_list()).set_index('symbol',
																								  inplace=True,
																								  drop=True)
	for i, r in coins.iterrows():
		if not Cryptocurrency.objects.filter(symbol__ilike=i).exists():
			Cryptocurrency.objects.create(symbol=i.lower(), name=r['name'].lower())
	print(f'Loaded {Cryptocurrency.objects.all().count() - n} cryptocurrencies from CoinGecko.')


def load_countries():
	countries = pycountry.countries
	n_upd = 0
	n = Country.objects.all().count()
	for obj in countries:
		if Country.objects.filter(name=obj.name).exists():
			Country.objects.get(name=obj.name).update(**dict(obj))
			n_upd += 1
		else:
			Country.objects.create(alpha_2=obj.alpha_2, alpha_3=obj.alpha_3, name=obj.name, numeric=obj.numeric,
								   official_name=obj.official_name)

	print(f'Added {Country.objects.all().count() - n} countries to database. \n'
		  f'Updated data for {n_upd} countries')


def load_currencies():
	currencies = pycountry.currencies
	n = FiatCurrency.objects.all().count()
	n_upd = 0
	for c in currencies.objects:
		if FiatCurrency.objects.filter(alpha_3=c.alpha_3).exists():
			FiatCurrency.objects.get(alpha_3=c.alpha_3).update(**dict(c))
			n_upd += 1
		else:
			FiatCurrency.objects.create(**dict(c))
	print(f'{FiatCurrency.objects.all().count() - n} fiat currencies have been added to database. \n'
		  f'{n_upd} fiat currencies have been updated.')


def map_currencies_to_countries():
	n = 0
	codes = country_currencies.CURRENCIES_BY_COUNTRY_CODE
	for country in Country.objects.all():
		alpha_3 = codes[country.alpha_2][0]
		if FiatCurrency.objects.filter(alpha_3=alpha_3).exists():
			currency = FiatCurrency.objects.get(alpha_3=alpha_3)
			if currency not in country.currencies.all():
				country.currencies.add(currency)
				country.save()
				n += 1
	print(f'Mapped {n} currencies to countries.')


def load_crypto_exchanges():
	n = CryptoExchange.objects.all().count()
	default_exchanges = str(DEFAULT_CRYPTO_EXCHANGES)
	for exchange_id in ccxt.exchanges:
		if re.search(exchange_id, default_exchanges):
			exchange_obj = getattr(ccxt, exchange_id)({'enableRateLimit': True})
			exchange_obj.load_markets()
			ex = CryptoExchange.objects.create(name=exchange_id, url=exchange_obj.urls['www'])
			for country_code in exchange_obj.countries:
				if Country.objects.filter(alpha_2=country_code).exists():
					ex.countries.add(Country.objects.get(alpha_2=country_code))
			ex.save()
		else:
			CryptoExchange.objects.create(name=exchange_id)
	print(f'Loaded {CryptoExchange.objects.all().count() - n} exchanges to database.')



def setup_crypto_db(exchange_id='binance', quote='USDT'):
	n = Cryptocurrency.objects.all().count()
	gecko = pycoingecko.CoinGeckoAPI()
	coins = pd.DataFrame(columns=['id', 'symbol', 'name'], data=gecko.get_coins_list()).set_index('symbol',
																								  inplace=True,
																								  drop=True)
	exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True})
	markets = pd.DataFrame(exchange.fetch_tickers()).transpose()
	markets = markets.loc[list(filter(lambda x: x.split('/')[1] == quote, markets.index))]['last']
	for i, v in markets.items():
		coin = i.split('/')[0].lower()
		try:
			name = coins.loc[coin, 'name']

		except:
			name = ''
		Cryptocurrency.objects.create(symbol=coin, name=name, price=v)
	print(f'Loaded {Cryptocurrency.objects.all().count() - n} cryptocurrencies to database.')





def connect_exchange(exchange_id, quote='USDT'):
	exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True})
	return pd.DataFrame(exchange.fetch_tickers()).transpose()


def filter_by_quote(ticker, quote='USDT'):
	return ticker.split('/')[1].__eq__(quote)


# def setup_fx_db():
#     code = None
#     currencies = country_currencies.CURRENCIES_BY_COUNTRY_CODE
#     fx_data = pd.read_csv('./data/iso-4217-currency-codes.csv').iloc[:, :3].set_index('Alphabetic_Code')
#     for obj in Country.objects.all():
#         codes = currencies[obj.alpha_2]
#         if not codes:
#             continue
#         code = codes[0]
#         if code not in fx_data.index:
#             continue
#
#         if not Currency.objects.filter(alpha_3=code).exists():
#             name = fx_data.at[code, 'Currency']
#             if isinstance(name, pd.Series):
#                 name = name.iloc[0]
#             curr = Currency.objects.create(alpha_3=code, name=name, country=obj)
#         else:
#             curr = Currency.objects.get(alpha_3=code)
#         obj.currency = curr
#         obj.save()
#     print('finito fx')


# coins = get_coins_info()[['Symbol', 'CoinName']]