
import pandas as pd
import numpy as np
from bokeh.layouts import gridplot
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, show, output_file


def get_rolling_mean(df,window=20):
    return df.rolling(window).mean()

def get_rolling_sd(df,window=20):
    return df.rolling(window).std()

def get_bollinger_bands(df, window=10):
    boll_df = pd.DataFrame(columns = ['boll_high', 'boll_low'])
    roll_mean = get_rolling_mean(df,window)
    roll_sd = get_rolling_sd(df,window)
    boll_df['boll_high'] = roll_mean + roll_sd *2
    boll_df['boll_low'] = roll_mean - roll_sd *2
    return boll_df

def get_daily_returns(df):
    daily_returns = ((df / df.shift(1))-1)*100
    daily_returns.iloc[0,:]=0
    mean = str(round(daily_returns.open.mean(),2))
    sd = str(round(daily_returns.open.std(),2))
    kurt = str(round(daily_returns.open.kurtosis(),2))
    return daily_returns, mean,sd,kurt

def build_plot(df, symbol, window=5, bins=26):
    inc = df.close > df.open
    dec = df.open > df.close
    df = df.drop(['s'], axis=1)
    boll_df = get_bollinger_bands(df.close,window)
    df = pd.concat([df,boll_df],axis=1)
    df2,mean,sd,kurt = get_daily_returns(df)
    hist, edges = np.histogram(df2.open, bins=bins)

    w = 12*60*60*8000
    x_axis_angle = 3.1426/4
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    timeseries = figure(title="One year History - " + symbol, 
                x_axis_type="datetime", 
                x_axis_label='Time', 
                y_axis_label='$',
                tools=TOOLS,
                plot_height=600, plot_width=600)
    timeseries.xaxis.formatter = DatetimeTickFormatter(
        seconds="%d %B %Y",
        minutes="%d %B %Y",
        hours="%d %b %Y",
        days="%d %b %Y",
        months="%d %b %Y",
        years="%d %b %Y"
    )
    timeseries.xaxis.major_label_orientation = x_axis_angle
    timeseries.line(df.stamp, df.close, legend_label="Closing price", line_width=2, line_color="gray", line_dash='solid')
    timeseries.line(df.stamp, df.high, legend_label="High price", line_width=1.25, line_color="green", line_dash='dashed')
    timeseries.line(df.stamp, df.low, legend_label="Low price", line_width=1.25, line_color="red", line_dash='dashed')

    candle = figure(title="One year History - Candle Plot : " + symbol, 
                x_axis_type="datetime", 
                x_axis_label='Time', 
                y_axis_label='$',
                tools=TOOLS,
                plot_height=600, plot_width=600)
    candle.xaxis.formatter = DatetimeTickFormatter(
        seconds="%d %B %Y",
        minutes="%d %B %Y",
        hours="%d %b %Y",
        days="%d %b %Y",
        months="%d %b %Y",
        years="%d %b %Y"
    )
    candle.grid.grid_line_alpha=0.3
    candle.xaxis.major_label_orientation = x_axis_angle
    candle.segment(df.stamp, df.high, df.stamp, df.low, color="black")
    candle.vbar(df.stamp[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    candle.vbar(df.stamp[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    bollinger = figure(title="One year History - Bollinger Bands :" + symbol, 
                x_axis_type="datetime", 
                x_axis_label='Time', 
                y_axis_label='$',
                tools=TOOLS,
                plot_height=600, plot_width=600)
    bollinger.xaxis.formatter = DatetimeTickFormatter(
        seconds="%d %B %Y",
        minutes="%d %B %Y",
        hours="%d %b %Y",
        days="%d %b %Y",
        months="%d %b %Y",
        years="%d %b %Y"
    )
    bollinger.xaxis.major_label_orientation = x_axis_angle
    bollinger.line(df.stamp, df.close, legend_label="Closing price", line_width=2, line_color="gray", line_dash='solid')
    bollinger.line(df.stamp, df.boll_high, legend_label="upper_bollinger", line_width=1.25, line_color="green", line_dash='dashed')
    bollinger.line(df.stamp, df.boll_low, legend_label="lower_bollinger", line_width=1.25, line_color="red", line_dash='dashed')

    returns = figure(title="One year History - Opening Price Returns : " + symbol +' mu : ' + mean + ' sd : ' + sd + ' kurt : '+ kurt, 
                x_axis_label='Returns %', 
                y_axis_label='Count',
                tools=TOOLS,
                plot_height=600, plot_width=600)
    returns.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color="skyblue", line_color="black")

    grid = gridplot([[timeseries, candle], [bollinger, returns]], width=600, height=600)
    return components(grid)