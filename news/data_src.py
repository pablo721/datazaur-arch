import investpy
from pycoingecko import CoinGeckoAPI
import requests
import os
import pandas as pd
from utils.decorators import load_or_save
import datetime

api_key = os.environ.get('CRYPTOCOMPARE_API_KEY')
url = f'https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key={api_key}'
filename = 'cryptocomp_news.csv'
refresh_rate = 86400





@load_or_save('cryptocomp_news.csv', 86400)
def cryptocomp_news():
    df = pd.json_normalize(requests.get(url).json()['Data'])[['published_on', 'title', 'url', 'source', 'body',
                                                              'categories']]
    df.loc[:, 'body'] = df.loc[:, 'body'].apply(lambda x: x[:320] + '...')

    df['title'] = df.apply(lambda x: f"""<a href="{x['url']}">{x['title']}</a>""", axis=1)
    df['published_on'] = df['published_on'].apply(lambda x: pd.to_datetime(x * 10 ** 9), True)
    df.drop('url', axis=1, inplace=True)
    df.columns = ['Date', 'Title', 'Source', 'Text', 'Categories']
    return df



@load_or_save('gecko_events.csv', 86400)
def gecko_events():
    data = []
    gecko = CoinGeckoAPI()
    events = gecko.get_events()['data']
    for event in events:
        data.append([event['description'], pd.DataFrame(pd.Series(event)).drop('description').transpose().to_html(escape=False, justify='center')])


    return data


#@load_or_save('gecko_global_metrics.csv', 86400)
def gecko_global_metrics():
    gecko = CoinGeckoAPI()
    data = gecko.get_global()
    return {'total_market_cap': data.pop('total_market_cap'),
            'total_volume': data.pop('total_volume'),
            'percentage_market_cap': data.pop('market_cap_percentage'),
            'numbers': data}



