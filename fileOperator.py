import os
import pandas as pd
from tkinter.filedialog import askopenfilename
from pandas import ExcelWriter

stockdir = './StockSymbols/'
stockfiles = {
	"NDAQ": 'NASDAQ.txt',	# NASDAQ
	"NYA": 'NYSE.txt',		# NYSE
	"XIU.TO": 'TSX.txt',	# TSX
	"TSXV": "TSXV.txt"		# TSXV
}

def get_stock_symbols(index):
    if index not in stockfiles.keys():
        print("Invalid index")
        return []

    stockpath = stockdir + stockfiles[index]
    stocks = []
    with open(stockpath, 'rt') as openedfile:
        for line in openedfile:
            stocks.append(line.split('\t')[0])
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

def remove_missing_stocks(missing, index):
	filename = stockfiles[index]
	with open(stockdir + filename) as oldfile, open(stockdir + "new" + filename, 'w') as newfile:
		for line in oldfile:
			if not any(value in line for value in missing):
				print(line)
				newfile.write(line)
	oldfile.close()
	newfile.close()
	replace_file_with(stockdir + filename, stockdir + "new" + filename)

def replace_file_with(old_name, new_name):
	os.remove(old_name)
	os.rename(new_name, old_name)