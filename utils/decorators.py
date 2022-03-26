import os
import datetime
import pandas as pd
import re
from utils.formatting import color_cell, add_hyperlinks
from website.models import Config


# decorator that checks if a file with data exists and whether it's recent enough (param refresh rate in seconds).
# refresh rate specifies (in seconds) how often files should be updated
def load_or_save(filename, refresh_rate=600):
    def decorator(func):
        def wraps(*args, **kwargs):
            if filename in os.listdir() and datetime.datetime.now().timestamp() - os.path.getmtime(filename) < refresh_rate:
                print(f'Data loaded from file: {filename}')
                return pd.read_csv(filename, index_col=0)
            else:
                print(f'Getting fresh data and updating file: {filename}')
                data = func(*args, **kwargs)
                df = pd.DataFrame(data)
                df.to_csv(filename)
                return data
        return wraps
    return decorator



@load_or_save('crypto.csv', 600)
def prep_crypto_display():
    def decorator(func):
        def wraps(*args, **kwargs):
            data = func(*args, **kwargs)
            for col in data.columns:
                if re.search(col, str(['Price', 'Δ', 'vol', 'cap', 'Supply'])):
                    data[col] = data[col].apply(lambda x: format(x, ','))
                    if 'Δ' in col:
                        data[col] = data[col].apply(color_cell)
            data = add_hyperlinks(data)
            if 'Url' in data.columns:
                data.drop('Url', inplace=True, axis=1)
            return data
        return wraps
    return decorator


