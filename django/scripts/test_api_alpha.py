import requests
import json
import os

KEY='ALPHA_VANTAGE_API_KEY'
key = os.environ.get(KEY)
function= 'CRYPTO_INTRADAY'
symbol = 'ETH'
market = 'USD'
interval = '5min'
url = 'https://www.alphavantage.co/query?function=' + function + '&symbol=' +symbol + '&market=' + market + '&interval=' + interval + '&apikey=' + key
r = requests.get(url)
data = r.json()
print(data)