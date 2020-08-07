import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

# stock = input("Enter a stock ticker symbol: ")
stock = "TSLA"
print(stock)

startyear = 2019
startmonth = 1
startday = 1

start = dt.datetime(startyear, startmonth, startday)
now = dt.datetime.now()

# Dataframe
df = pdr.get_data_yahoo(stock, start, now)

# moving_average = 50

# sma_string = "Sma_" + str(moving_average)

# # Creates column with moving average using the from the 4th column of dataframe (Adjusted Close)
# dataframe[sma_string] = dataframe.iloc[:, 4].rolling(window=moving_average).mean()

# dataframe = dataframe.iloc[moving_average:]

# Exponential Moving Averages
shortEmas = [3, 5, 8, 10, 12, 15]
longEmas = [30, 35, 40, 45, 50, 60]
emasUsed = shortEmas + longEmas

for ema in emasUsed:
    df["Ema_"+str(ema)] = round(df["Adj Close"].ewm(span=ema, adjust=False).mean(), 2)

print(df.tail())



pos = 0 # Entering position: 1 (Y), 0 (N)
num = 0 # Row
percent_change_results = [] # Result of trade

for i in df.index:
    shortValues = map(lambda ema : df["Ema_" + str(ema)][i], shortEmas)
    longValues = map(lambda ema : df["Ema_" + str(ema)][i], longEmas)
    cmin = min(shortValues)
    cmax = max(longValues)

    close = df["Adj Close"][i]

    # Red White Blue
    if cmin > cmax:
        print("Red White Blue")
        if (pos == 0):
            buy_price = close
            pos = 1
            print("Buying now at " + str(buy_price))

    # Blue White Red
    elif cmin < cmax:
        print("Blue White Red")
        if (pos == 1):
            sell_price = close
            pos = 0
            print("Selling now at " + str(sell_price))
            percent_change = (sell_price/buy_price - 1) * 100
            percent_change_results.append(percent_change)

    # Open position at end of pandas dataframe
    if num == df["Adj Close"].count()-1:
        if (pos == 1):
            sell_price = close
            pos = 0
            print("Selling now at " + str(sell_price))
            percent_change = (sell_price/buy_price - 1) * 100
            percent_change_results.append(percent_change)

    num += 1

print(percent_change_results)

gains = 0
num_gains = 0
losses = 0
num_losses = 0
total_return = 1

for result in percent_change_results:
    if result > 0:
        gains += result
        num_gains += 1
    else: 
        losses += result
        num_losses += 1
    total_return = total_return * ((result/100) + 1)

total_return = round((total_return - 1) * 100, 2)

if (num_gains > 0):
    avg_gain = gains/num_gains
    max_return = str(max(percent_change_results))
else:
    avg_gain=0
    max_return = "undefined"

if (num_losses > 0):
    avg_loss = losses/num_losses
    max_loss = str(min(percent_change_results))
    ratio = str(-avg_gain/avg_loss)
else:
    avg_loss=0
    max_loss = "undefined"
    ratio = "inf"

if (num_gains > 0 or num_losses > 0):
    batting_avg = num_gains/(num_gains + num_losses)
else:
    batting_avg = 0

print("""
    Results for {stock} going back to {date}, Sample size: {trade_count} trades
    EMAs used: {emas}
    Batting Avg: {batting_avg}
    Gain/Loss ratio: {ratio}
    Average Gain: {avg_gain}
    Average Loss: {avg_loss}
    Max Return: {max_r}
    Max Loss: {max_l}
    Total return over {trade_count} trades: {total_return}%
""".format(
    stock = stock, 
    date = str(df.index[0]), 
    trade_count = str(num_gains + num_losses), 
    emas = str(emasUsed), 
    batting_avg = batting_avg,
    ratio = ratio,
    avg_gain = avg_gain,
    avg_loss = avg_loss,
    max_r = max_return,
    max_l = max_loss,
    total_return = total_return
))