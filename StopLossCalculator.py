"""
Stop Loss Calculator:
* (1) Percentage Method: -6%
* (2) Support Method: gets most recent support and get value slightly below
* (3) Moving Average Method: gets long-term moving average price and get value slightly below
"""
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf
from yahoo_fin import stock_info as si
from indicators import get_average_true_range, get_support_level

yf.pdr_override()

def percentage_method(stock):
    try:
        price = si.get_live_price(stock)
        return round(price * 0.94, 2)
    except Exception as e:
        print("Error calculating stop loss with percentage for " + stock)
        print(e)

def support_method(stock):
    try:
        return round(get_support_level(stock, 1) - get_average_true_range(stock), 2)
    except Exception as e:
        print("Error calculating stop loss with support method for " + stock)
        print(e)

# Select a trend based on whether you're riding a short, medium, long-term trend
def moving_average_method(stock, trend = "LONG"):
    trends = {
        "SHORT": 20,
        "MED": 50,
        "LONG": 200
    }
    start = dt.datetime.now() - dt.timedelta(days=365)
    now = dt.datetime.now()
    
    try:
        df = pdr.get_data_yahoo(stock, start, now)
        df["SMA"] = round(df["Adj Close"].rolling(window=trends[trend]).mean(), 2)
        ma = df["SMA"][-1]
        return round(ma - get_average_true_range(stock), 2)
    except Exception as e:
        print("Error calculating stop loss with moving average for " + stock)
        print(e)