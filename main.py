import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

stock = input("Enter a stock ticker symbol: ")
print(stock)

startyear = 2019
startmonth = 1
startday = 1

start = dt.datetime(startyear, startmonth, startday)
now = dt.datetime.now()

dataframe=pdr.get_data_yahoo(stock, start, now)

moving_average = 50

sma_string = "Sma_" + str(moving_average)

# Creates column with moving average using the from the 4th column of dataframe (Adjusted Close)
dataframe[sma_string] = dataframe.iloc[:, 4].rolling(window=moving_average).mean()

dataframe = dataframe.iloc[moving_average:]

higher = 0
lower = 0

for i in dataframe.index:
    if (dataframe["Adj Close"][i] > dataframe[sma_string][i]):
        print("The Close is higher")
        higher+=1
    else:
        print("The Close is lower")
        lower+=1

print(str(higher))
print(str(lower))