import yfinance as yf
import pandas as pd
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf
import util as util

yf.pdr_override()

start = dt.datetime.now() - dt.timedelta(days=365)
now = dt.datetime.now()
index_change_dict = {}


def get_relative_strength(stock, index, data = None):
    if data == None:
        stock_data = pdr.get_data_yahoo(stock, start, now)
    else:
        stock_data = data

    stock_old = stock_data["Adj Close"][0]
    stock_now = stock_data["Adj Close"][-1]
    stock_change = util.get_percent_change(stock_now, stock_old)    

    if (index in index_change_dict):
        index_change = index_change_dict[index]
    else:
        index_data = pdr.get_data_yahoo(index, start, now)
        index_old = index_data["Adj Close"][0]
        index_now = index_data["Adj Close"][-1]
        index_change = util.get_percent_change(index_now, index_old)
        index_change_dict[index] = index_change

    return round(stock_change/index_change * 100, 2)

"""
Average True Range (ATR) is a technical indicator that measures market volatility,
typically derived from a moving average of a series of ATRs.
The maximum of:
- The current high less the current low
- The absolute value of the current high less the previous close
- The absolute value of the current low less the previous close
"""
def get_average_true_range(stock):
    sum = 0
    days = 14
    df = pdr.get_data_yahoo(stock, start, now)
    for i in range(1, days):
        currHigh = df["High"][-i]
        currLow = df["Low"][-i]
        prevClose = df["Adj Close"][-i-1]
        sum += max(currHigh - currLow, abs(currHigh - prevClose), abs(currLow - prevClose))
    return round(sum/days, 2)

def get_resistance_level(stock, level):
    df = pdr.get_data_yahoo(stock, start, now)

    high = df["High"][-1]
    low = df["Low"][-1]
    close = df["Adj Close"][-1]

    pivot = (high + low + close)/3
    switch = {
        1: (2 * pivot) - low,
        2: pivot - low + high,
        3: high + 2 * (pivot - low),
        4: high + 3 * (pivot - low)
    }
    return switch.get(level)

def get_support_level(stock, level):
    df = pdr.get_data_yahoo(stock, start, now)

    high = df["High"][-1]
    low = df["Low"][-1]
    close = df["Adj Close"][-1]

    pivot = (high + low + close)/3
    switch = {
        1: 2 * pivot - high,
        2: pivot - high + low,
        3: low - 2 * (high - pivot),
        4: low - 3 * (high - pivot)
    }
    return switch.get(level)