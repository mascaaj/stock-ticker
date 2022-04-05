from wsgiref.util import request_uri
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from .data_processing import build_plot
from .interface import get_stock, get_yr_historical_data
import pandas as pd

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