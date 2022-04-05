import requests
import json
import os
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
from bokeh.models import DatetimeTickFormatter
import pandas as pd


KEY = 'FINHUB_API_KEY'
key = str(os.environ.get(KEY))
symbol = 'AMZN'
resolution = 'W'
url_rtprice = 'https://finnhub.io/api/v1/quote?symbol=' + symbol + '&token=' + key
url_profile = 'https://finnhub.io/api/v1/stock/profile2?symbol=' + symbol + '&token=' + key
url_financials = 'https://finnhub.io/api/v1/stock/metric?symbol=' + symbol + '&metric=all&token=' + key
url_history = 'https://finnhub.io/api/v1/stock/candle?symbol=' + symbol + '&resolution=' + resolution +'&from=1617570568&to=1649106568&token=' + key
# api_request_price = requests.get(url_rtprice)
# api_profile = requests.get(url_profile)
# api_financials = requests.get(url_financials)
api_history = requests.get(url_history)
api = json.loads(api_history.content)
# api.update(api_profile.json())
# api.update(api_financials.json())
# x = [datetime.fromtimestamp(int(ts)).date() for ts in api.get('t')]

# df = pd.DataFrame([ts*1000 for ts in api.get('t')])
df = pd.DataFrame(api)
# , columns =['close', 'high', 'low','open','status','timestamp','volume'])
df = df.rename(columns={"c": "close", "o": "open", "h":"high", "l":"low", "v":"vol","t":"timestamp"})
df.timestamp = df.timestamp*1000
w = 12*60*60*10000
inc = df.close > df.open
dec = df.open > df.close
# print(df)
print(inc)



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
p.line(df.timestamp, df.high, legend_label="High price", line_width=1.25, line_color="green", line_dash='dashed')
p.line(df.timestamp, df.low, legend_label="Low price", line_width=1.25, line_color="red", line_dash='dashed')

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

h = figure(title="One year History - " + symbol, x_axis_type="datetime", x_axis_label='Time', y_axis_label='$',
             plot_height=800, plot_width=800)
h.xaxis.formatter = DatetimeTickFormatter(
    seconds="%d %B %Y",
    minutes="%d %B %Y",
    hours="%d %b %Y",
    days="%d %b %Y",
    months="%d %b %Y",
    years="%d %b %Y"
)
# g.xaxis.major_label_orientation = pi/4
h.grid.grid_line_alpha=0.3

h.segment(df.timestamp, df.high, df.timestamp, df.low, color="black")
h.dash(df.timestamp, df.open, color="green", size=10, legend_label="Open Price")
h.dash(df.timestamp, df.close, color="red", size=10,  legend_label="Close Price")


# g.segment(df.timestamp, df.high, df.timestamp, df.low, color="black")
# g.vbar(df.timestamp[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
# g.vbar(df.timestamp[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")



grid = gridplot([[p, g], [h, q]], width=800, height=800)
show(grid)