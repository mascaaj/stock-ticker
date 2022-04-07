import requests
import json
import os
import time
import pandas as pd
from datetime import datetime, timedelta


class InterfaceLayer:

    def __init__(self, symbol, resolution='W', delta=365, years=1):
        _key = 'FINHUB_API_KEY'
        self.key = str(os.environ.get(_key))
        self.symbol = str(symbol)
        self.years = years
        self.url_rtprice = 'https://finnhub.io/api/v1/quote?symbol=' +\
                            self.symbol + '&token=' + self.key
        self.url_profile = 'https://finnhub.io/api/v1/stock/profile2?symbol=' +\
                            self.symbol + '&token=' + self.key
        self.url_financials = 'https://finnhub.io/api/v1/stock/metric?symbol=' +\
                            self.symbol + '&metric=all&token=' + self.key
        self.resolution = resolution
        self.api = "initialized, not used"
        self.calculate_start_date(delta=delta*years)

    def calculate_start_date(self, delta=365):
        now = time.time()
        self.now_ts = str(int(now))
        self.now_dt = datetime.fromtimestamp(now)
        self.start_stamp = str(int((self.now_dt - timedelta(days=delta)).timestamp()))
        self.url_history = 'https://finnhub.io/api/v1/stock/candle?symbol=' +\
                self.symbol + '&resolution=' + self.resolution +\
                '&from='+ self.start_stamp + '&to=' + self.now_ts +\
                '&token=' + self.key
        self.url_indicator_rsi = 'https://finnhub.io/api/v1/indicator?symbol=' +\
                self.symbol + '&resolution=' + self.resolution +\
                '&from='+ self.start_stamp + '&to=' + self.now_ts +\
                '&indicator='+ 'rsi' + '&timeperiod='+ '3' + '&token=' + self.key

    # API Interface Layer
    def get_stock(self):
        api_request_price = requests.get(self.url_rtprice)
        api_profile = requests.get(self.url_profile)
        api_financials = requests.get(self.url_financials)
        try:
            self.api = json.loads(api_request_price.content)
            # Might be a better way to raise this error, need to study json parser
            if not self.api.get('d'):
                raise ValueError
            self.api.update(api_profile.json())
            self.api.update(api_financials.json())
        except Exception as e:
            self.api = 'Error ...'

    def get_yr_historical_data(self):
        api_history = requests.get(self.url_indicator_rsi)
        try:
            self.api = json.loads(api_history.content)
            # Might be a better way to raise this error, need to study json parser
            if not self.api.get('o'):
                raise ValueError
        except Exception as e:
            self.api = 'Error ...'
        self.df = pd.DataFrame(self.api)
        self.df = self.df.rename(columns={"c": "close", "o": "open", "h":"high",
                                 "l":"low", "v":"vol","t":"stamp"})
        self.df.stamp = self.df.stamp*1000

    def get_indicator(self):
        self.df['sma_3'] = self.df['close'].rolling(3).mean()
        self.df['sma_10'] = self.df['close'].rolling(10).mean()
        self.df['sma_20'] = self.df['close'].rolling(20).mean()
        self.df['ema_30'] = self.df['close'].ewm(span=30).mean()