import io
import requests
import pandas as pd

import get_all_tickers

from get_all_tickers import get_tickers

headers = {
    'authority': 'api.nasdaq.com',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'origin': 'https://www.nasdaq.com',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.nasdaq.com/',
    'accept-language': 'en-US,en;q=0.9',
}

def params(exchange): 
    return (
    ('tableonly', 'true'),
    ('offset', '0'),
    ('exchange', exchange),
    ('download', 'true'),
)

def params_region(region):
    return (
        ('tableonly', 'true'),
        ('offset', '0'),
        ('region', region),
        ('download', 'true'),
    )

def exchange2df(exchange):
    r = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers, params=params(exchange))
    data = r.json()['data']
    df = pd.DataFrame(data['rows'], columns=data['headers'])

    # I'm doing this because the rest of the package uses 'Symbol' not 'symbol'
    df.columns = [x.title() for x in df.columns]
    return df

def get_tickers_by_region(region):
    if region in Region:
        response = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers,
                                params=params_region(region))
        data = io.StringIO(response.text)
        df = pd.read_csv(data, sep=",")
        return __exchange2list(df)
    else:
        raise ValueError('Please enter a valid region (use a Region.REGION as the argument, e.g. Region.AFRICA)')

get_tickers.headers = headers
get_tickers.params = params
get_tickers.__exchange2df = exchange2df
get_tickers.get_tickers_by_region = get_tickers_by_region