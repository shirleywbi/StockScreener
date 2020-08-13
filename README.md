# StockScreener

Based on Richard Moglen's Python for Finance Youtube Series
<https://www.youtube.com/watch?v=myFD0np9eys&list=PLPfme2mwsQ1FQhH1icKEfiYdLSUHE-Wo5&index=1>

## Stock Screener

List of stock symbols were retrieved from <http://www.eoddata.com/> for the following exchanges:

- NYSE
- TSX
- TSXV
- NASDAQ

Last updated: 2020-08-09

To improve the speed of the Stock Screener, run `processing.py` beforehand. This script removes stock symbols that are not compatible with the python package used.

## Stop Loss Calculator

According to Investopedia, there are several ways to determine where to set your stop-loss:

1. The **percentage method** limits the stop-loss at a specific percentage (e.g., 6%)
2. The **support method** limits the stop-loss slightly below the most recent support level
3. The **moving average method** places the stop-loss slightly below a longer-term moving average price
