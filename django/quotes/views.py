from wsgiref.util import request_uri
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
import requests
import json
import os
import pandas as pd
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, show, output_file


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
        key = os.environ.get(KEY)
        symbol = str(symbol)
        resolution = 'W'
        url_history = 'https://finnhub.io/api/v1/stock/candle?symbol=' + symbol + '&resolution=' + resolution +'&from=1617570568&to=1649106568&token=' + key
        api_history = requests.get(url_history)
        try:
            api = json.loads(api_history.content)
            # Might be a better way to raise this error, need to study json parser
            if not api.get('o'):
                raise ValueError
        except Exception as e:
            api = 'Error ...'
        df = pd.DataFrame(api)
        df = df.rename(columns={"c": "close", "o": "open", "h":"high", "l":"low", "v":"vol","t":"timestamp"})
        df.timestamp = df.timestamp*1000
        return df


# Application Layer

def home(request):
    if request.method == 'POST':
        ticker =  request.POST["ticker"]
        api = get_stock(ticker)
        return render(request, 'home.html', {'api' : api})
    else:
        return render(request, 'home.html', {'ticker' : "Enter a ticker symbol above."})

def add_stocks(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock has been added.")
            return redirect('add-stocks')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api = get_stock(ticker_item)
            output.append(api)
        return render(request, 'add_stocks.html', {'ticker':ticker, 'output':output})

def delete(request, stock_id):
    item =  Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, "Stock has been deleted.")
    return redirect('delete-stocks')

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stocks.html', {'ticker':ticker})

def about(request): 
    return render(request, 'about.html', {})

def plot_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'plot_stocks.html', {'ticker' : ticker})

def plot(request, stock):
    df = get_yr_historical_data(str(stock))
    script, div = build_plot(df, stock)
    ticker = Stock.objects.all()
    return render(request, 'plot_stocks.html', {'ticker': ticker, 'script': script, 'div':div})

def build_plot(df, symbol):
    inc = df.close > df.open
    dec = df.open > df.close
    w = 12*60*60*8000
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(title="One year History - " + symbol, 
                x_axis_type="datetime", 
                x_axis_label='Time', 
                y_axis_label='$',
                tools=TOOLS,
                plot_height=600, plot_width=600)
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

    q = figure(title="One year History - " + symbol, 
                x_axis_type="datetime", 
                x_axis_label='Time', 
                y_axis_label='$',
                tools=TOOLS,
                plot_height=600, plot_width=600)
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

    g = figure(title="One year History - " + symbol, 
                x_axis_type="datetime", 
                x_axis_label='Time', 
                y_axis_label='$',
                tools=TOOLS,
                plot_height=600, plot_width=600)
    g.xaxis.formatter = DatetimeTickFormatter(
        seconds="%d %B %Y",
        minutes="%d %B %Y",
        hours="%d %b %Y",
        days="%d %b %Y",
        months="%d %b %Y",
        years="%d %b %Y"
    )
    g.grid.grid_line_alpha=0.3
    g.segment(df.timestamp, df.high, df.timestamp, df.low, color="black")
    g.vbar(df.timestamp[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    g.vbar(df.timestamp[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    h = figure(title="One year History - " + symbol, 
                x_axis_type="datetime", 
                x_axis_label='Time', 
                y_axis_label='$',
                tools=TOOLS,
                plot_height=600, plot_width=600)
    h.xaxis.formatter = DatetimeTickFormatter(
        seconds="%d %B %Y",
        minutes="%d %B %Y",
        hours="%d %b %Y",
        days="%d %b %Y",
        months="%d %b %Y",
        years="%d %b %Y"
    )
    h.grid.grid_line_alpha=0.3

    h.segment(df.timestamp, df.high, df.timestamp, df.low, color="black")
    h.dash(df.timestamp, df.open, color="green", size=10, legend_label="Open Price")
    h.dash(df.timestamp, df.close, color="red", size=10,  legend_label="Close Price")
    grid = gridplot([[p, g], [h, q]], width=600, height=600)
    return components(grid)