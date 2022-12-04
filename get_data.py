# documentation to help know how to use the python module: 
#  https://python-tradingview-ta.readthedocs.io/en/latest/usage.html
#  https://tvdb.brianthe.dev/

from tradingview_ta import TA_Handler, Interval
import itertools
from openpyxl import Workbook
import csv

NASDAQ_symbols = ['CSX', 'AMD', 'GOOGL', 'AMZN', 'DBX', 'AAPL', 'SBUX', 'MSFT', 'CSCO', 'TSCO', 'NVDA']
NYSE_symbols = ['BAC', 'SYF', 'IBM', 'DKS', 'KR', 'UNH', 'DUK', 'TM', 'CNI', 'V', 'DE', 'FE', 'MA', 'O', 'LMT', 'WMT', 'DGX', 'WM', 'GIS', 'JPM', 'T', 'ABBV', 'JNJ', 'VALE', 'LOW', 'LEN', 'CVX', 'XOM', 'CAT', 'NKE']

stock_data = []


# Get the data for all stocks
for sym in NASDAQ_symbols:
    request = TA_Handler(screener='america', exchange='NASDAQ', symbol=sym)
    output = request.get_analysis().indicators
    new_dict = {}
    new_dict['symbol'] = sym
    new_dict['price'] = output['close']
    new_dict['RSI'] = output['RSI']
    new_dict['pivot middle'] = output['Pivot.M.Classic.Middle']
    new_dict['pivot support 1'] = output['Pivot.M.Classic.S1']
    new_dict['pivot support 2'] = output['Pivot.M.Classic.S2']
    
    stock_data.append(new_dict)

for sym in NYSE_symbols:
    request = TA_Handler(screener='america', exchange='NYSE', symbol=sym)
    output = request.get_analysis().indicators
    new_dict = {}
    new_dict['symbol'] = sym
    new_dict['price'] = output['close']
    new_dict['RSI'] = output['RSI']
    new_dict['pivot middle'] = output['Pivot.M.Classic.Middle']
    new_dict['pivot support 1'] = output['Pivot.M.Classic.S1']
    new_dict['pivot support 2'] = output['Pivot.M.Classic.S2']

    stock_data.append(new_dict)


# Dictionary keys: ['Recommend.Other', 'Recommend.All', 'Recommend.MA', 'RSI', 'RSI[1]', 'Stoch.K', 'Stoch.D', 'Stoch.K[1]', 'Stoch.D[1]', 'CCI20', 'CCI20[1]', 
# 'ADX', 'ADX+DI', 'ADX-DI', 'ADX+DI[1]', 'ADX-DI[1]', 'AO', 'AO[1]', 'Mom', 'Mom[1]', 'MACD.macd', 'MACD.signal', 'Rec.Stoch.RSI', 'Stoch.RSI.K', 'Rec.WR', 'W.R', 
# 'Rec.BBPower', 'BBPower', 'Rec.UO', 'UO', 'close', 'EMA5', 'SMA5', 'EMA10', 'SMA10', 'EMA20', 'SMA20', 'EMA30', 'SMA30', 'EMA50', 'SMA50', 'EMA100', 'SMA100', 'EMA200', 
# 'SMA200', 'Rec.Ichimoku', 'Ichimoku.BLine', 'Rec.VWMA', 'VWMA', 'Rec.HullMA9', 'HullMA9', 'Pivot.M.Classic.S3', 'Pivot.M.Classic.S2', 'Pivot.M.Classic.S1', 'Pivot.M.Classic.Middle', 
# 'Pivot.M.Classic.R1', 'Pivot.M.Classic.R2', 'Pivot.M.Classic.R3', 'Pivot.M.Fibonacci.S3', 'Pivot.M.Fibonacci.S2', 'Pivot.M.Fibonacci.S1', 'Pivot.M.Fibonacci.Middle', 
# 'Pivot.M.Fibonacci.R1', 'Pivot.M.Fibonacci.R2', 'Pivot.M.Fibonacci.R3', 'Pivot.M.Camarilla.S3', 'Pivot.M.Camarilla.S2', 'Pivot.M.Camarilla.S1', 'Pivot.M.Camarilla.Middle', 
# 'Pivot.M.Camarilla.R1', 'Pivot.M.Camarilla.R2', 'Pivot.M.Camarilla.R3', 'Pivot.M.Woodie.S3', 'Pivot.M.Woodie.S2', 'Pivot.M.Woodie.S1', 'Pivot.M.Woodie.Middle', 'Pivot.M.Woodie.R1', 
# 'Pivot.M.Woodie.R2', 'Pivot.M.Woodie.R3', 'Pivot.M.Demark.S1', 'Pivot.M.Demark.Middle', 'Pivot.M.Demark.R1', 'open', 'P.SAR', 'BB.lower', 'BB.upper', 'AO[2]', 'volume', 'change', 
# 'low', 'high']
 

# Determine if stock is 'good' to sell a put on
# A stock is determined good if the RSI is below 50, and the price of the stock is below the middle pivot point

good_stocks = []

for stock in stock_data:
    if (float(stock['RSI']) < 50):
        if (float(stock['price'])) < (float(stock['pivot middle'])):
            good_stocks.append(stock)

# Output data to CSV file

keys = good_stocks[0].keys()

with open('./results/Good_Stocks.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(good_stocks)




