import os
import pandas as pd
from tkinter.filedialog import askopenfilename
from pandas import ExcelWriter

def get_stock_symbols():
    stockpath = './StockSymbols/'
    stockfiles = [
        'NASDAQ.txt',
        'NYSE.txt',
        'TSX.txt'
    ]

    stocks = set()
    for stockfile in stockfiles:
        with open(stockpath + stockfile, 'rt') as openedfile:
            for line in openedfile:
                stocks.add(line.split('\t')[0])
        openedfile.close()
    return stocks

def get_spreadsheet_rows_with_dialog():
	ftypes = [(".xlsm","*.xlsx",".xls")] # can accept these dialog files
	ttl  = "Title"
	dir1 = 'C:\\'
	filePath = askopenfilename(filetypes = ftypes, initialdir = dir1, title = ttl)
	return pd.read_excel(filePath)

def write_file(filename, content):
	dirname = os.path.dirname(__file__)
	new_file = os.path.join(dirname, "ScreenOutput.xlsx")
	writer = ExcelWriter(new_file)
	content.to_excel(writer, "Sheet1")
	writer.save()