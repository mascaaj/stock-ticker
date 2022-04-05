import requests
import json
import os
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
from bokeh.models import DatetimeTickFormatter
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

KEY = 'FINHUB_API_KEY'
key = str(os.environ.get(KEY))
plotting = True
symbol = 'NVDA'
resolution = 'W'

now = datetime.fromtimestamp(time.time())
start_stamp = now - timedelta(days=365)
start_stamp = str(int(start_stamp.timestamp()))

url_rtprice = 'https://finnhub.io/api/v1/quote?symbol=' + symbol + '&token=' + key
url_profile = 'https://finnhub.io/api/v1/stock/profile2?symbol=' + symbol + '&token=' + key
url_financials = 'https://finnhub.io/api/v1/stock/metric?symbol=' + symbol + '&metric=all&token=' + key
url_history = 'https://finnhub.io/api/v1/stock/candle?symbol=' + symbol + '&resolution=' + resolution +'&from='+ start_stamp + '&to=' + str(int(time.time()))+'&token=' + key
# api_request_price = requests.get(url_rtprice)
# api_profile = requests.get(url_profile)
# api_financials = requests.get(url_financials)
api_history = requests.get(url_history)
api = json.loads(api_history.content)
# api.update(api_profile.json())
# api.update(api_financials.json())


df = pd.DataFrame(api)
df = df.rename(columns={"c": "close", "o": "open", "h":"high", "l":"low", "v":"vol","t":"timestamp"})
df.timestamp = df.timestamp*1000
w = 12*60*60*10000
inc = df.close > df.open
dec = df.open > df.close
print(inc)

def normalize_data(df):
    """Normalize data with respect to first entry in the dataframe"""
    return df/df.iloc[0,:]

def get_rolling_mean(df,window=3):
    return df.rolling(window).mean()

def get_rolling_sd(df,window=3):
    return df.rolling(window).std()

def get_daily_returns(df):
    daily_returns = ((df / df.shift(1))-1)*100
    daily_returns.iloc[0,:]=0
    return daily_returns

def get_bollinger_bands(df, window=10):
    boll_df = pd.DataFrame(columns = ['boll_high', 'boll_low'])
    roll_mean = get_rolling_mean(df,window)
    roll_sd = get_rolling_sd(df,window)
    bh = roll_mean + roll_sd *2
    bl = roll_mean - roll_sd *2
    boll_df['boll_high'] = bh
    boll_df['boll_low'] = bl
    return boll_df

df = df.drop(['s'], axis=1)
boll_df = get_bollinger_bands(df.close,5)
df = pd.concat([df,boll_df],axis=1)
df2 = get_daily_returns(df)
hist, edges = np.histogram(df2.open,bins=26)
mean = df2.open.mean()
sd = df2.open.std()
kurt = df2.open.kurtosis()
if plotting:
    p = figure(title="One year History - " + symbol, x_axis_type="datetime", x_axis_label='Time', y_axis_label='$',
                plot_height=800, plot_width=800)
    p.xaxis.formatter = DatetimeTickFormatter(
        seconds="%d %B %Y",
        minutes="%d %B %Y",
        hours="%d %b %Y",
        days="%d %b %Y",
        months="%d %b %Y",
        years="%d %b %Y"
    )
    p.line(df.timestamp, df.close, legend_label="Closing price", line_width=2, line_color="gray", line_dash='solid')
    p.line(df.timestamp, df.boll_high, legend_label="High Boll", line_width=1.25, line_color="green", line_dash='dashed')
    p.line(df.timestamp, df.boll_low, legend_label="Low Boll", line_width=1.25, line_color="red", line_dash='dashed')

    q = figure(title="One year History - " + symbol, x_axis_type="datetime", x_axis_label='Time', y_axis_label='$',
                plot_height=800, plot_width=800)
    q.xaxis.formatter = DatetimeTickFormatter(
        seconds="%d %B %Y",
        minutes="%d %B %Y",
        hours="%d %b %Y",
        days="%d %b %Y",
        months="%d %b %Y",
        years="%d %b %Y"
    )
    q.line(df.timestamp, df.close, legend_label="Closing price", line_width=2, line_color="gray", line_dash='solid')
    q.line(df.timestamp, df.high, legend_label="High price", line_width=1.25, line_color="green", line_dash='dashed')
    q.line(df.timestamp, df.low, legend_label="Low price", line_width=1.25, line_color="red", line_dash='dashed')



    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    g = figure(title="One year History - " + symbol, x_axis_type="datetime", x_axis_label='Time', y_axis_label='$',
                plot_height=800, plot_width=800)
    g.xaxis.formatter = DatetimeTickFormatter(
        seconds="%d %B %Y",
        minutes="%d %B %Y",
        hours="%d %b %Y",
        days="%d %b %Y",
        months="%d %b %Y",
        years="%d %b %Y"
    )
    # g.xaxis.major_label_orientation = pi/4
    g.grid.grid_line_alpha=0.3

    # g.segment(df.timestamp, df.high, df.timestamp, df.low, color="black")
    # g.dash(df.timestamp, df.open, color="green", size=10, legend_label="Open Price")
    # g.dash(df.timestamp, df.close, color="red", size=10,  legend_label="Close Price")


    g.segment(df.timestamp, df.high, df.timestamp, df.low, color="black")
    g.vbar(df.timestamp[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    g.vbar(df.timestamp[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    h = figure(title="One year History - " + symbol, x_axis_label='Normalized Price', y_axis_label='$',
                plot_height=800, plot_width=800)
    h.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color="skyblue", line_color="white")


    # g.segment(df.timestamp, df.high, df.timestamp, df.low, color="black")
    # g.vbar(df.timestamp[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    # g.vbar(df.timestamp[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")



    grid = gridplot([[p, g], [h, q]], width=800, height=800)
    show(grid)