import pandas as pd
import numpy as np
import requests
import os
import json
import datetime
import ccxt

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/counts/recent"

# Optional params: start_time,end_time,since_id,until_id,next_token,granularity
query_params = {'query': '#ETH', 'granularity': 'minute'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentTweetCountsPython"
    return r


def connect_to_endpoint(params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def tweet_count(query_params):
    json_response = connect_to_endpoint(query_params)
    df = pd.DataFrame(json_response['data'])
    df = df[['start', 'end', 'tweet_count']]
    since = ccxt.Exchange.parse8601(df.loc[0, 'start'])
    df[['start', 'end']] = df[['start', 'end']].applymap(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M'))
    return df, since


def get_prices(ticker, exchange, interval, since):
    exchange = getattr(ccxt, exchange)()
    data = []
    count = 0
    while True:
        d2 = exchange.fetch_ohlcv(ticker, interval, since)
        data += d2
        count += 1
        if len(d2) <= 1:
            break
        else:
            since = d2[-1][0]
    df = pd.DataFrame(data)
    df.drop_duplicates(subset=0, inplace=True)
    df.name = ticker + '_' + exchange.id + '_' + interval
    # df.set_index(0, inplace=True)
    return df


def get_corr_matrix(df):
    matrix = pd.DataFrame(columns=df.columns, index=df.columns)
    matrix.index.name = 'corr matrix'
    for col in df.columns:
        for col2 in df.columns:
            matrix.loc[col, col2] = df[col].corr(df[col2]).__round__(3)
    return matrix

