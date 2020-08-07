import os
import functools
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pandas import ExcelWriter

yf.pdr_override()
start =dt.datetime(2017,12,1)
now = dt.datetime.now()

root = Tk()
ftypes = [(".xlsm","*.xlsx",".xls")] # can accept these dialog files
ttl  = "Title"
dir1 = 'C:\\'
filePath = askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl)

stocklist = pd.read_excel(filePath)

exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])

for i in stocklist.index:
	stock = str(stocklist["Symbol"][i])
	RS_Rating = stocklist["RS Rating"][i]

	try:
		df = pdr.get_data_yahoo(stock, start, now)

		smaUsed=[50, 150, 200]
		for sma in smaUsed:
			df["SMA_" + str(sma)] = round(df["Adj Close"].rolling(window=sma).mean(), 2)

		currentClose = df["Adj Close"][-1]
		moving_average_50 = df["SMA_50"][-1]
		moving_average_150 = df["SMA_150"][-1]
		moving_average_200 = df["SMA_200"][-1]
		low_of_52week = min(df["Adj Close"][-260:])
		high_of_52week = max(df["Adj Close"][-260:])

		try:
			moving_average_200_20past = df["SMA_200"][-20]
		except Exception:
			moving_average_200_20past = 0

		print("Checking " + stock + ".....")

		"""
		Mark Minervini's Trend Template:
		(1) Current Price > 150 SMA and > 200 SMA
		(2) 150 SMA and > 200 SMA
		(3) 200 SMA trending up for at least 1 month (ideally 4-5 months)
		(4) 50 SMA > 150 SMA and 50 SMA > 200 SMA
		(5) Current Price > 50 SMA
		(6) Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation)
		(7) Current Price is within 25% of 52 week high
		(8) IBD RS rating > 70 and the higher the better
		"""
		conditions = [
			currentClose > moving_average_150 and currentClose > moving_average_200,
			moving_average_150 > moving_average_200,
			moving_average_200 > moving_average_200_20past,
			moving_average_50 > moving_average_150 and moving_average_50 > moving_average_200,		
			currentClose > moving_average_50,
			currentClose > 1.3 * low_of_52week,
			currentClose > 0.75 * high_of_52week,
			RS_Rating > 70,
		]

		conditions_met = functools.reduce(lambda result, cond : result and cond, conditions)

		if conditions_met:
			exportList = exportList.append({'Stock': stock, "RS_Rating": RS_Rating, "50 Day MA": moving_average_50, "150 Day Ma": moving_average_150, "200 Day MA": moving_average_200, "52 Week Low": low_of_52week, "52 week High": high_of_52week}, ignore_index=True)
	
	except Exception:
		print("No data on " + stock)

print(exportList)

dirname = os.path.dirname(__file__)
new_file = os.path.join(dirname, "ScreenOutput.xlsx")
writer = ExcelWriter(new_file)
exportList.to_excel(writer, "Sheet1")
writer.save()