# retrieves all of the technical indicators needed to determine buy and sell signals

# documentation to help know how to use the python module: 
#  https://python-tradingview-ta.readthedocs.io/en/latest/usage.html
#  https://tvdb.brianthe.dev/
#  https://python-tradingview-ta.readthedocs.io/_/downloads/en/latest/pdf/
#  https://pastebin.com/1DjWv2Hd

from tradingview_ta import TA_Handler, Interval
import ta
import itertools
import csv
import pandas as pd

def get_tech_indicators(NYSE_symbols, NASDAQ_symbols):
    '''
    Input:

    NYSE_symbols - list of strings

    NASDAQ_symbols - list of strings

    Output:

    list of dictionaries with keys - Symbol, Price, RSI, Pivot middle, Pivot support 1, Pivot support 2, MACD_line, MACD_signal, Keltner lower, Keltner upper Chart Link
    '''
    stock_data = []

    # Get the data for all stocks
    print ("\nCollecting data for all stocks...\n")
    for sym in NASDAQ_symbols:
        request = TA_Handler(screener='america', exchange='NASDAQ', symbol=sym, interval=Interval.INTERVAL_1_DAY)
        request.add_indicators(indicators=["KltChnl.lower", "KltChnl.upper"])
        output = request.get_indicators()
        new_dict = {}
        new_dict['Symbol'] = sym
        new_dict['Price'] = output['close']
        new_dict['RSI'] = output['RSI']
        new_dict['Pivot middle'] = output['Pivot.M.Classic.Middle']
        new_dict['Pivot support 1'] = output['Pivot.M.Classic.S1']
        new_dict['Pivot support 2'] = output['Pivot.M.Classic.S2']
        new_dict['MACD_line'] = output['MACD.macd']
        new_dict['MACD_signal'] = output['MACD.signal']
        try:
            new_dict['Keltner lower'] = output['KltChnl.lower']
            new_dict['Keltner upper'] = output['KltChnl.upper']
        except:
            new_dict['Keltner lower'] = 10000000
            new_dict['Keltner upper'] = 0

        new_dict['Chart Link'] = 'https://finance.yahoo.com/quote/' + str(sym) + '/chart?p=' + str(sym)
        
        stock_data.append(new_dict)

    for sym in NYSE_symbols:
        request = TA_Handler(screener='america', exchange='NYSE', symbol=sym, interval=Interval.INTERVAL_1_DAY)
        request.add_indicators(indicators=["KltChnl.lower", "KltChnl.upper"])
        output = request.get_indicators()
        new_dict = {}
        new_dict['Symbol'] = sym
        new_dict['Price'] = output['close']
        new_dict['RSI'] = output['RSI']
        new_dict['Pivot middle'] = output['Pivot.M.Classic.Middle']
        new_dict['Pivot support 1'] = output['Pivot.M.Classic.S1']
        new_dict['Pivot support 2'] = output['Pivot.M.Classic.S2']
        new_dict['MACD_line'] = output['MACD.macd']
        new_dict['MACD_signal'] = output['MACD.signal']
        try:
            new_dict['Keltner lower'] = output['KltChnl.lower']
            new_dict['Keltner upper'] = output['KltChnl.upper']
        except:
            new_dict['Keltner lower'] = 10000000
            new_dict['Keltner upper'] = 0
        new_dict['Chart Link'] = 'https://finance.yahoo.com/quote/' + str(sym) + '/chart?' 
        
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

    return(stock_data)


