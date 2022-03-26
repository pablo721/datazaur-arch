import requests
import json
import pandas as pd
import numpy as np
import os

key = os.environ.get('finnhub_key')
stock = 'TSLA'

r = requests.get(f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={stock}&token={key}")

test = json.loads(r.text)

df = pd.DataFrame(test['data'])

df.to_csv('df66.csv')
