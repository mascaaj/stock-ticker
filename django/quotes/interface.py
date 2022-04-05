import requests
import json
import os
import time
import pandas as pd
from datetime import datetime, timedelta

KEY = 'FINHUB_API_KEY'

# API Interface Layer
def get_stock(symbol):
    key = os.environ.get(KEY)
    symbol = str(symbol)
    url_rtprice = 'https://finnhub.io/api/v1/quote?symbol=' + symbol + '&token=' + key
    url_profile = 'https://finnhub.io/api/v1/stock/profile2?symbol=' + symbol + '&token=' + key
    url_financials = 'https://finnhub.io/api/v1/stock/metric?symbol=' + symbol + '&metric=all&token=' + key
    api_request_price = requests.get(url_rtprice)
    api_profile = requests.get(url_profile)
    api_financials = requests.get(url_financials)
    try:
        api = json.loads(api_request_price.content)
        # Might be a better way to raise this error, need to study json parser
        if not api.get('d'):
            raise ValueError
        api.update(api_profile.json())
        api.update(api_financials.json())
    except Exception as e:
        api = 'Error ...'
    return api

def get_yr_historical_data(symbol):
    now = datetime.fromtimestamp(time.time())
    start_stamp = now - timedelta(days=365)
    start_stamp = str(int(start_stamp.timestamp()))
    key = os.environ.get(KEY)
    symbol = str(symbol)
    resolution = 'W'
    url_history = 'https://finnhub.io/api/v1/stock/candle?symbol=' + symbol + '&resolution=' + resolution +'&from='+ start_stamp + '&to=' + str(int(time.time()))+'&token=' + key
    api_history = requests.get(url_history)
    try:
        api = json.loads(api_history.content)
        # Might be a better way to raise this error, need to study json parser
        if not api.get('o'):
            raise ValueError
    except Exception as e:
        api = 'Error ...'
    df = pd.DataFrame(api)
    df = df.rename(columns={"c": "close", "o": "open", "h":"high", "l":"low", "v":"vol","t":"stamp"})
    df.stamp = df.stamp*1000
    return df

def get_5yr_historical_data(symbol):
    now = datetime.fromtimestamp(time.time())
    start_stamp = now - timedelta(days=365*5)
    start_stamp = str(int(start_stamp.timestamp()))
    key = os.environ.get(KEY)
    symbol = str(symbol)
    resolution = 'W'
    url_history = 'https://finnhub.io/api/v1/stock/candle?symbol=' + symbol + '&resolution=' + resolution +'&from='+ start_stamp + '&to=' + str(int(time.time()))+'&token=' + key
    api_history = requests.get(url_history)
    try:
        api = json.loads(api_history.content)
        # Might be a better way to raise this error, need to study json parser
        if not api.get('o'):
            raise ValueError
    except Exception as e:
        api = 'Error ...'
    df = pd.DataFrame(api)
    df = df.rename(columns={"c": "close", "o": "open", "h":"high", "l":"low", "v":"vol","t":"stamp"})
    df.stamp = df.stamp*1000
    return df