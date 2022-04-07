import requests
import json
import os
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot
from bokeh.models import DatetimeTickFormatter, LinearAxis, Range1d, Span
from bokeh.embed import components


class InterfaceLayer:
    
    def __init__(self, symbol, resolution='W', delta=2*365):
        _key = 'FINHUB_API_KEY'
        self.key = str(os.environ.get(_key))
        self.symbol = str(symbol)
        self.url_rtprice = 'https://finnhub.io/api/v1/quote?symbol=' +\
                            self.symbol + '&token=' + self.key
        self.url_profile = 'https://finnhub.io/api/v1/stock/profile2?symbol=' +\
                            self.symbol + '&token=' + self.key
        self.url_financials = 'https://finnhub.io/api/v1/stock/metric?symbol=' +\
                            self.symbol + '&metric=all&token=' + self.key
        
        self.resolution = resolution
        self.api = "initialized, not used"
        self.calculate_start_date(delta=delta)



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
        self.df = self.df.rename(columns={"c": "close", "o": "open", "h":"high", "l":"low", "v":"vol","t":"stamp"})
        self.df.stamp = self.df.stamp*1000

    def get_indicator(self):
        self.df['sma_3'] = self.df['close'].rolling(3).mean()
        self.df['sma_10'] = self.df['close'].rolling(10).mean()
        self.df['sma_20'] = self.df['close'].rolling(20).mean()
        self.df['ema_30'] = self.df['close'].ewm(span=30).mean()


class GeneratePlots:

    def __init__(self, df, symbol, window=8, bins=30):
        self.window = window
        self.symbol = symbol
        self.bins=bins
        self.df = df.drop(['s'], axis=1)
        self.get_bollinger_bands()
        self.get_daily_returns()
        # Might move to plot class
        self.bar_width = 12*60*60*8000
        self.x_axis_angle = 3.1426/4
        self.df = pd.concat([self.df,self.boll_df],axis=1)
        self.tools = "pan,wheel_zoom,box_zoom,reset,save"

    def get_rolling_mean_close(self):
        return self.df.close.rolling(self.window).mean()

    def get_rolling_sd_close(self):
        return self.df.close.rolling(self.window).std()

    def get_bollinger_bands(self):
        self.boll_df = pd.DataFrame(columns = ['boll_high', 'boll_low'])
        roll_mean = self.get_rolling_mean_close()
        roll_sd = self.get_rolling_sd_close()
        self.boll_df['boll_high'] = roll_mean + roll_sd * 2
        self.boll_df['boll_low'] = roll_mean - roll_sd * 2

    def get_daily_returns(self):
        self.daily_returns = ((self.df / self.df.shift(1)) - 1) * 100
        self.daily_returns.iloc[0, :] = 0
        self.mean = str(round(self.daily_returns.open.mean(), 2))
        self.sd = str(round(self.daily_returns.open.std(), 2))
        self.kurt = str(round(self.daily_returns.open.kurtosis(), 2))

    def timeseries_plot(self):
        
        self.timeseries = figure(title="One year History - " + self.symbol, 
                    x_axis_type="datetime", 
                    x_axis_label='Time', 
                    y_axis_label='$',
                    tools=self.tools,
                    plot_height=600, plot_width=600)
        self.timeseries.xaxis.formatter = DatetimeTickFormatter(
            seconds="%d %B %Y",
            minutes="%d %B %Y",
            hours="%d %b %Y",
            days="%d %b %Y",
            months="%d %b %Y",
            years="%d %b %Y"
        )
        self.timeseries.xaxis.major_label_orientation = self.x_axis_angle
        self.timeseries.line(self.df.stamp, self.df.close, 
                            legend_label="Closing price", line_width=2, 
                            line_color="gray", line_dash='solid')
        self.timeseries.line(self.df.stamp, self.df.high, 
                            legend_label="High price", line_width=1.25, 
                            line_color="green", line_dash='dashed')
        self.timeseries.line(self.df.stamp, self.df.low, 
                            legend_label="Low price", line_width=1.25, 
                            line_color="red", line_dash='dashed')


    def candle_plot(self):
        inc = self.df.close > self.df.open
        dec = self.df.open > self.df.close
        self.candle = figure(title="One year History - Candle Plot : " + 
                        self.symbol, 
                        x_axis_type="datetime", 
                        x_axis_label='Time', 
                        y_axis_label='$',
                        tools=self.tools,
                        plot_height=600, plot_width=600)
        self.candle.xaxis.formatter = DatetimeTickFormatter(
            seconds="%d %B %Y",
            minutes="%d %B %Y",
            hours="%d %b %Y",
            days="%d %b %Y",
            months="%d %b %Y",
            years="%d %b %Y"
        )
        self.candle.xaxis.major_label_orientation = self.x_axis_angle
        self.candle.segment(self.df.stamp, self.df.high, self.df.stamp, 
                            self.df.low, color="black")
        self.candle.vbar(self.df.stamp[inc], self.bar_width, self.df.open[inc], 
                            self.df.close[inc], fill_color="#D5E1DD", 
                            line_color="black")
        self.candle.vbar(self.df.stamp[dec], self.bar_width, self.df.open[dec], 
                            self.df.close[dec], fill_color="#F2583E", 
                            line_color="black")


    def indicators_plot(self):
        
        self.indicators = figure(title="One year History - " + self.symbol, 
                    x_axis_type="datetime", 
                    x_axis_label='Time', 
                    y_axis_label='$',
                    tools=self.tools,
                    plot_height=600, plot_width=600)
        self.indicators.xaxis.formatter = DatetimeTickFormatter(
            seconds="%d %B %Y",
            minutes="%d %B %Y",
            hours="%d %b %Y",
            days="%d %b %Y",
            months="%d %b %Y",
            years="%d %b %Y"
        )

        low, high  = self.df[['open', 'close']].min().min(), self.df[['open', 'close']].max().max()
        diff = high-low
        self.indicators.y_range = Range1d(low-0.1*diff, high+0.1*diff)
        self.indicators.xaxis.major_label_orientation = self.x_axis_angle
        self.indicators.line(self.df.stamp, self.df.close, 
                            legend_label="Closing price", line_width=0.8, 
                            line_color="gray", line_dash='solid')
        self.indicators.line(self.df.stamp, self.df.sma_3, 
                            legend_label="sma-3", line_width=2, 
                            line_color="green", line_dash='dashed')
        self.indicators.line(self.df.stamp, self.df.sma_10, 
                            legend_label="sma-10", line_width=1.25, 
                            line_color="black", line_dash='dashed')
        self.indicators.line(self.df.stamp, self.df.sma_20, 
                            legend_label="sma-20", line_width=1.25, 
                            line_color="blue", line_dash='dashed')
        self.indicators.line(self.df.stamp, self.df.ema_30, 
                            legend_label="ema-30", line_width=1.25, 
                            line_color="orange", line_dash='dashed')
        self.indicators.legend.location = "top_left"
        self.indicators.extra_y_ranges.update({'two':  Range1d(0, 1.1*self.df.vol.max())})
        self.indicators.add_layout(LinearAxis(y_range_name='two'), 'right')
        self.indicators.vbar(self.df.stamp, self.bar_width, self.df.vol, [0]*self.df.shape[0], 
                            alpha=0.25, level='underlay', y_range_name='two')

    def rsi_plot(self):
        
        self.rsi = figure(title="One year History - rsi" + self.symbol, 
                    x_axis_type="datetime", 
                    x_axis_label='Time', 
                    y_axis_label='$',
                    tools=self.tools,
                    plot_height=600, plot_width=600)
        self.rsi.xaxis.formatter = DatetimeTickFormatter(
            seconds="%d %B %Y",
            minutes="%d %B %Y",
            hours="%d %b %Y",
            days="%d %b %Y",
            months="%d %b %Y",
            years="%d %b %Y"
        )

        self.rsi.xaxis.major_label_orientation = self.x_axis_angle
        self.rsi.line(self.df.stamp, self.df.rsi, 
                            legend_label="RSI", line_width=1.2, 
                            line_color="gray", line_dash='solid')
        hline_70 = Span(location=70, dimension='width', line_color='red', line_width=0.5)
        hline_30 = Span(location=30, dimension='width', line_color='green', line_width=0.5)
        self.rsi.add_layout(hline_70)
        self.rsi.add_layout(hline_30)

    def bollinger_plot(self):
        self.bollinger = figure(title="One year History - Bollinger Bands :" + 
                    self.symbol, 
                    x_axis_type="datetime", 
                    x_axis_label='Time', 
                    y_axis_label='$',
                    tools=self.tools,
                    plot_height=600, plot_width=600)
        self.bollinger.xaxis.formatter = DatetimeTickFormatter(
            seconds="%d %B %Y",
            minutes="%d %B %Y",
            hours="%d %b %Y",
            days="%d %b %Y",
            months="%d %b %Y",
            years="%d %b %Y"
        )
        self.bollinger.xaxis.major_label_orientation = self.x_axis_angle
        self.bollinger.line(self.df.stamp, self.df.close, 
                            legend_label="Closing price", line_width=2, 
                            line_color="gray", line_dash='solid')
        self.bollinger.line(self.df.stamp, self.df.boll_high, 
                            legend_label="upper_bollinger", line_width=1.25, 
                            line_color="green", line_dash='dashed')
        self.bollinger.line(self.df.stamp, self.df.boll_low, 
                            legend_label="lower_bollinger", line_width=1.25, 
                            line_color="red", line_dash='dashed')

    def returns_histogram(self):
        hist, edges = np.histogram(self.daily_returns.open, bins=self.bins)
        self.returns = figure(title="One year History - Opening Returns : " 
                        + self.symbol +
                        ' mu : ' + self.mean + 
                        ' sd : ' + self.sd + 
                        ' kurt : '+ self.kurt, 
                        x_axis_label='Returns %', 
                        y_axis_label='Count',
                        tools=self.tools,
                        plot_height=600, plot_width=600)
        self.returns.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
                fill_color="skyblue", line_color="black")


    def build_plot(self, width=600, height=600):
        self.grid = gridplot([[self.timeseries, self.candle], 
                            [self.bollinger, self.returns], 
                            [self.indicators, self.rsi]], 
                            width=width, height=height)
        self.components = components(self.grid)

    def plot(self):
        self.timeseries_plot()
        self.indicators_plot()
        self.rsi_plot()
        self.candle_plot()
        self.bollinger_plot()
        self.returns_histogram()
        self.build_plot()
        show(self.grid)
        return self.components

if __name__ == "__main__":
    symbol = 'CAT'
    stock = InterfaceLayer(symbol)
    stock.get_yr_historical_data()
    stock.get_indicator()

    plots = GeneratePlots(stock.df,symbol)
    plots.plot()