
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about.html', views.about, name='about'),
    path('add_stocks.html', views.add_stocks, name='add-stocks'),
    path('delete/<stock_id>', views.delete, name='delete'),
    path('delete_stocks.html', views.delete_stock, name='delete-stocks'),
    path('plot/<stock>', views.plot, name='plot'),
    path('plot_stocks.html', views.plot_stock, name='plot-stocks'),
]
