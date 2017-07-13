import googlefinance
import yahoo_finance
import json

stockData = json.loads(open('./data/stocks.json').read())

def stockSum(stockAmounts):
    sumOfIt = 0
    index = 0
    for i in stockAmounts:
        sumOfIt += float(i['LastTradePrice']) * stockData['owned'][index]['quantity']
        index += 1
    return sumOfIt

def retrieveStocks(symbols):
    stockAmounts = googlefinance.getQuotes(map(lambda x: x['symbol'], stockData['owned']))
    return stockAmounts

def historicalRetreive(symbols, timestamp):
    toBuild = True
    return True

def currentProfits():
    putIn = stockData['totalInvested']
    activelyUsed = putIn - stockData['uninvested']
    stockValue = stockSum(retrieveStocks(stockData['owned']))
    return stockValue - activelyUsed

def netAssets():
    return stockSum(retrieveStocks(stockData['owned']))
