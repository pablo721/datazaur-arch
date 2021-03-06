
import pandas as pd
import pycountry
import country_currencies
import ccxt
from pycoingecko import CoinGeckoAPI
import yaml
import json
import re
from markets.models import *
from website.models import *
from crypto.models import *
from economics.models import *
from data import constants
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
			Config.objects.get(key=k).value=v
			n_upd += 1
		else:
			Config.objects.create(key=k, value=v)
	print(f'Added {Config.objects.all().count() - n} parameters to database. \n'
		  f'Updated {n_upd} parameters.')



def setup_all():
	funcs = [load_config, load_countries, load_currencies, map_currencies, load_cryptocomp_coins, load_crypto_exchanges]
	tables = ['website_config', 'economics_country', 'markets_currency', 'markets_currency', 'crypto_cryptocurrency',
			  'crypto_cryptoexchange']
	try:
		for func, table in zip(funcs, tables):
			func()
			Updates.objects.get(table=table).timestamp = datetime.datetime.now()
	except Exception as e:
		print(f'Error: {e}')



def load_cryptocomp_coins():
	n = Cryptocurrency.objects.all().count()
	coins = get_coins_info().loc[:, ['Symbol', 'CoinName', 'Description', 'Algorithm', 'ProofType', 'AssetWebsiteUrl']]
	coins.columns = ['symbol', 'name', 'description', 'hash_algorithm', 'proof_type', 'url']
	coins[['description', 'url']] = coins[['description', 'url']].apply(lambda x: x[:254])
	for i, row in coins.iterrows():
		if not Cryptocurrency.objects.filter(symbol=row['symbol']).exists():
			try:
				Cryptocurrency.objects.create(name=row['name'], symbol=row['symbol'], url=str(row['url'])[:254] if row['url'] else '',
											  description=str(row['description'])[:254] if row['description'] else '',
											  hash_algorithm=row['hash_algorithm'], proof_type=row['proof_type'])
			except:
				continue
	print(f'Loaded {Cryptocurrency.objects.all().count() - n} cryptocurrencies from Cryptocompare.')



def load_tickers(exchanges=constants.DEFAULT_CRYPTO_EXCHANGES):
	url = f'https://min-api.cryptocompare.com/data/v4/all/exchanges?api_key={API_KEY}'



def load_gecko_coins():
	n = Cryptocurrency.objects.all().count()
	gecko = CoinGeckoAPI()
	coins = pd.DataFrame(columns=['id', 'symbol', 'name'], data=gecko.get_coins_list()).set_index('symbol',
																								  inplace=True,
																								  drop=True)
	for i, r in coins.iterrows():
		if not Cryptocurrency.objects.filter(symbol__ilike=i).exists():
			Cryptocurrency.objects.create(symbol=i.lower(), name=r['name'].lower())
	print(f'Loaded {Cryptocurrency.objects.all().count() - n} cryptos from CoinGecko.')


def load_countries():
	countries = pycountry.countries
	n = Country.objects.all().count()
	for obj in countries:
		if not Country.objects.filter(name=obj.name).exists():
			Country.objects.create(alpha_2=obj.alpha_2, name=obj.name)
	print(f'Loaded {Country.objects.all().count() - n} countries to db. \n')


def load_currencies():
	currencies = pycountry.currencies
	n = Currency.objects.all().count()
	n_upd = 0
	for c in currencies:
		try:
			if Currency.objects.filter(alpha_3=c.alpha_3).exists():
				Currency.objects.get(alpha_3=c.alpha_3).update(name=c.name)
				n_upd += 1
			else:
				Currency.objects.create(name=c.name[:125], alpha_3=c.alpha_3)
		except Exception as e:
			print(f'Error {e}')
			continue
	print(f'Added {Currency.objects.all().count() - n}  currencies to db. \n'
		  f'Updated {n_upd}  currencies.')


def map_currencies():
	n = 0
	codes = {k: v[0] if v else None for k, v in country_currencies.CURRENCIES_BY_COUNTRY_CODE.items()}
	for country in Country.objects.all():
		alpha_3 = codes[country.alpha_2]
		if Currency.objects.filter(alpha_3=alpha_3).exists() and not country.currencies.filter(alpha_3=alpha_3).exists():
			currency = Currency.objects.get(alpha_3=alpha_3)
			country.currencies.add(currency)
			country.save()
			n += 1
	print(f'Mapped {n} currencies to countries.')


def load_crypto_exchanges():
	n = CryptoExchange.objects.all().count()
	default_exchanges = str(constants.DEFAULT_CRYPTO_EXCHANGES)
	for exchange_id in ccxt.exchanges:
		if re.search(exchange_id, default_exchanges):
			exchange_obj = getattr(ccxt, exchange_id)({'enableRateLimit': True})
			exchange_obj.load_markets()
			ex = CryptoExchange.objects.create(name=exchange_id, url=exchange_obj.urls['www'][:255])
			for country_code in exchange_obj.countries:
				if Country.objects.filter(alpha_2=country_code).exists():
					ex.countries.add(Country.objects.get(alpha_2=country_code))
			ex.save()
		else:
			CryptoExchange.objects.create(name=exchange_id)
	print(f'Loaded {CryptoExchange.objects.all().count() - n} exchanges to database.')



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