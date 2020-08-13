import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf
import time as time

import fileOperator as fo


yf.pdr_override()

def remove_missing_stocks_from_files():
    indexes = ["NDAQ", "NYA", "XIU.TO"]
    checked_stocks = set()
    missing_stocks = set()

    start = dt.datetime.now() - dt.timedelta(days=7)
    now = dt.datetime.now()

    for index in indexes:
        stocklist = fo.get_stock_symbols(index)

        for stock in stocklist:
            if stock not in checked_stocks:
                try:
                    df = pdr.get_data_yahoo(stock, start, now)
                    if df.empty:
                        missing_stocks.add(stock)
                except Exception:
                    missing_stocks.add(stock)
                finally:
                    checked_stocks.add(stock)

        if len(missing_stocks) != 0:
            fo.remove_missing_stocks(missing_stocks, index)
            missing_stocks = set()


start_time = time.time()
remove_missing_stocks_from_files()
processing_time = time.time() - start_time
print("Processed in: " + str(round(processing_time, 2)) + "s")