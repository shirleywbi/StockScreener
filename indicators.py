import yfinance as yf
import pandas as pd
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf
import util as util

yf.pdr_override()

def get_relative_strength(stock, index):
    start = dt.datetime.now() - dt.timedelta(days=365)
    now = dt.datetime.now()

    stock_data = pdr.get_data_yahoo(stock, start, now)
    stock_old = stock_data["Adj Close"][0]
    stock_now = stock_data["Adj Close"][-1]
    stock_change = util.get_percent_change(stock_now, stock_old)    

    index_data = pdr.get_data_yahoo(index, start, now)
    index_old = index_data["Adj Close"][0]
    index_now = index_data["Adj Close"][-1]
    index_change = util.get_percent_change(index_now, index_old)

    return round(stock_change/index_change * 100, 2)

rs = get_relative_strength("MSFT", "NDAQ")
print(rs)