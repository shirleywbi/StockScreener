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