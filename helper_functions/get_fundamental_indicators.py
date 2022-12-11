# retrieves all of the technical indicators needed to determine buy and sell signals
exec("""\nimport sys,os\nexec(\"\"\"\\ndef get_git_root(path=os.getcwd(),display=False):\\n    \\n    '''\\n    Get Git Root Directory. Only recursively goes up 10 directories.\\n    RETURNS: None or absolute path to git root directory\\n    '''\\n    count = 0\\n    prefix = ""\\n    while count < 10:\\n        if os.path.exists(prefix+'.git'):\\n            return os.path.abspath(prefix)\\n        else:\\n            prefix +="../"\\n            count+=1\\n    print("No git top level directory")\\n    return None\\n\"\"\")\ngitroot=get_git_root()\nsys.path.append(os.path.abspath(gitroot))\n""") # one liner statement that adds the root of this repo to python for inports
from helper_functions import general
from importlib import reload
reload(general)

import os
import json
import requests
import time
import pandas as pd
import yfinance as yf #https://github.com/ranaroussi/yfinance

def get_all_symbols():
    general.get_env_vars()

    # cache all symbols
    symbol_cache = general.dataPath("all_stock_symbols.pkl")
    symbols = general.fileLoadCache(symbol_cache)
    if symbols is None:
        nasdaq = json.loads((requests.get("https://eodhistoricaldata.com/api/exchange-symbol-list/NASDAQ?fmt=json&api_token="+os.environ['symbols_api_key'])).content)
        nyse = json.loads((requests.get("https://eodhistoricaldata.com/api/exchange-symbol-list/NYSE?fmt=json&api_token="+os.environ['symbols_api_key'])).content)
        symbols = nasdaq+nyse
        general.fileSaveCache(symbol_cache, symbols)

    ## 'Code', 'Name', and 'Exchange' are the useful variables
    print("There are a total of: "+str(len(symbols))+" symbols")
    return symbols

# this downloads symbol data for the past:
#  symbol "info" takes 3 seconds to download. 9.3 hours total
#  symbol (% changes last 5 years, 4 quarters earnings info)
def get_symbol_data():
    ticker_list = get_all_symbols()
    stock_data = []
    for ticker in ticker_list[]:
        data = yf.Ticker(ticker['Code'])
        stock_data.append({"data":data, "exchange":ticker['Exchange']})
    return stock_data

def large_cap(market_cap):
    if market_cap is None:
        return False
    if market_cap >= 15000000000:
        return True
    else:
        return False
def good_pe_ratio(ratio):
    if ratio is None:
        return False
    if ratio <= 30:
        return True
    else:
        return False
def good_pb_ratio(ratio):
    if ratio is None:
        return False
    if ratio <= 10:
        return True
    else:
        return False
def good_dividend(dividend):
    if dividend is None:
        return False
    if dividend > 2:
        return True
    else:
        return False

def keys_not_missing(keys):
    required_keys = ['shortName', 'symbol', 'currentPrice', 'marketCap', 'forwardEps', 'trailingEps', 'forwardPE',
     'trailingPE', 'priceToBook', 'profitMargins', 'totalRevenue', 'grossProfits', 'returnOnAssets', 'returnOnEquity', 'debtToEquity', 'sharesOutstanding', 'floatShares']
    if set(required_keys).issubset(set(keys)):
        return True
    else:
        return False

def is_increasing(dictionary):
    # must feed a value of ['Revenue'] or ['Earnings']
    # Get a list of the dictionary keys (assumed to represent years)
    years = list(dictionary.keys())

    # Sort the list of years in ascending order
    years.sort()

    # Loop over the years and their corresponding values in the dictionary
    for year, value in dictionary.items():
        # If the current year is the first year, there is no previous year to compare to
        if year == years[0]:
            continue
        # Get the index of the current year in the sorted list of years
        index = years.index(year)

        # Get the value for the previous year in the dictionary
        prev_value = dictionary[years[index - 1]]

        # If the value for the current year is not greater than the value for the previous year, return False
        if value <= prev_value:
            return False
    # If all of the values in the dictionary are increasing, return True
    return True

def get_stock_percentage_change(stock_oject, time):
    history = stock_oject.history(period=time)
    current = history['Close'][-1]
    old = history['Close'][0]
    return (current-old)/old

def write_symbols_to_csv(cache=False):
    start_time = time.time()
    stocks = get_symbol_data()
    # cache these results
    stock_data_path = general.dataPath("all_stock_data.pkl")
    if cache:
        stock_data = general.fileLoadCache(stock_data_path)
    else:
        stock_data = []

    if stock_data == []:
        #stocks[63:64] is ACGL which matches my filters for testing
        for stock in stocks:
            info = stock['data'].info
            if keys_not_missing(info.keys()):
                good_stock = {}
                # Basic info
                good_stock['shortName'] = info['shortName']
                good_stock['industry'] = info['industry']
                good_stock['symbol'] = info['symbol']
                good_stock['currentPrice'] = info['currentPrice']
                good_stock['marketCap'] = info['marketCap']

                # Dividends
                good_stock['dividendYield'] = info['dividendYield'] #0.0272=2.72%
                exDividendDate = info['exDividendDate']
                if exDividendDate is not None:
                    from datetime import datetime
                    good_stock['exDividendDate'] = datetime.utcfromtimestamp(int(exDividendDate)).strftime('%c')
                else:
                    good_stock['exDividendDate'] = None

                # EPS
                good_stock['forwardEps'] = info['forwardEps']
                good_stock['trailingEps'] = info['trailingEps']
                # P/E ratio
                good_stock['forwardPE'] = info['forwardPE']
                good_stock['trailingPE'] = info['trailingPE']
                # P/B ratio
                good_stock['priceToBook'] = info['priceToBook']

                # profit info
                good_stock['profitMargins'] = info['profitMargins']
                good_stock['totalRevenue'] = info['totalRevenue']
                good_stock['grossProfits'] = info['grossProfits']
                good_stock['returnOnAssets'] = info['returnOnAssets']
                good_stock['returnOnEquity'] = info['returnOnEquity']
                good_stock['debtToEquity'] = info['debtToEquity']
                good_stock['sharesOutstanding'] = info['sharesOutstanding']
                good_stock['floatShares'] = info['floatShares']

                # Only search these things if above filters are good
                if large_cap(info['marketCap']) and good_pb_ratio(info['priceToBook']) and good_pe_ratio(info['forwardPE']):
                    print(info['symbol']+" stock good")
                    # next earnings date
                    # 'Value'
                    nextEarningsDate = (stock['data'].calendar).to_dict()[0]['Earnings Date']
                    good_stock['nextEarningsDate'] = nextEarningsDate

                    # Quarterly income
                    earnings_info = (stock['data'].get_earnings(freq="quarterly")).to_dict()
                    good_stock['4Quarters_increasing_revenue'] = is_increasing(earnings_info['Revenue'])
                    good_stock['4Quarters_increasing_profit'] = is_increasing(earnings_info['Revenue'])
                    
                    # Yearly income
                    earnings_info = (stock['data'].get_earnings(freq="yearly")).to_dict()
                    good_stock['4years_increasing_revenue'] = is_increasing(earnings_info['Revenue'])
                    good_stock['4years_increasing_profit'] = is_increasing(earnings_info['Earnings'])
                    
                    # Changes last: 1 week, 1 month, 3 months, 6 months, 1 year, 5 year
                    good_stock['pct_chg_5y'] = get_stock_percentage_change(stock['data'], "5y")
                    good_stock['pct_chg_1y'] = get_stock_percentage_change(stock['data'], "1y")
                    good_stock['pct_chg_6mo'] = get_stock_percentage_change(stock['data'], "6mo")
                    good_stock['pct_chg_3mo'] = get_stock_percentage_change(stock['data'], "3mo")
                    good_stock['pct_chg_1mo'] = get_stock_percentage_change(stock['data'], "1mo")
                    good_stock['pct_chg_1wk'] = get_stock_percentage_change(stock['data'], "1wk")
                    
                    # Google finance link
                    url = "https://g.co/finance/"+info['symbol']+":"+stock['exchange']
                    good_stock['lookup'] = url

                    stock_data.append(good_stock)
            #else:
                #print(str(info.get('symbol'))+" has missing values...skipping")
        general.fileSaveCache(stock_data_path, stock_data)
        print("--- %s seconds to get all stock data  ---" % (round(time.time() - start_time,2)))
    # write to CSV
    stock_csv_path = general.resultsPath("all_stock_data.csv")
    general.listOfDictsToCSV(stock_data, stock_csv_path)
    return stock_data



