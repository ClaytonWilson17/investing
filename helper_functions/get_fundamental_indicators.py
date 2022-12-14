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
from datetime import datetime

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
#  symbol (% changes last 5 years, 4 quarters earnings info) takes 1.7 sec
def get_all_symbol_object():
    ticker_list = get_all_symbols()
    stock_data = []
    for ticker in ticker_list:
        data = yf.Ticker(ticker['Code'])
        stock_data.append({"data":data, "exchange":ticker['Exchange']})
    return stock_data

def get_symbol_object(stock_code, exchange):
    data = yf.Ticker(stock_code)
    stock_data = {"data":data, "exchange":exchange}
    return stock_data

def large_cap(market_cap):
    if market_cap is None:
        return False
    if market_cap >= 15000000000:
        return True
    else:
        return False
def affordable_price(price):
    if price <= 200:
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
    if ratio <= 12:
        return True
    else:
        return False
def good_dividend(dividend):
    if dividend is None:
        return False
    if dividend == "":
        return False
    if float(dividend) > .02: #2%
        return True
    else:
        return False
def good_instutional_ownership(ratio):
    if float(ratio) > .6:
        return True
    else:
        return False
def good_debt_ratio(debtToAssetsRatio):
    if debtToAssetsRatio < 1:
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

def quarter_to_datetime(quarter):
  # Extract the year and quarter from the quarter year string
  year = int(quarter[-4:])
  quarter = int(quarter[0])
  
  # Calculate the month of the quarter year
  month = (quarter - 1) * 3 + 1
  
  # Return a datetime object for the quarter year
  return datetime(year, month, 1)

# say it is increasing if within 2 percent
def is_increasing(dictionary):
    # must feed a value of ['Revenue'] or ['Earnings']
    # Get a list of the dictionary keys (assumed to represent years)
    years = list(dictionary.keys())

    # Sort the list of years in ascending order. Sort years and quarters differently
    quarters = False
    for value in years:
        if isinstance(value, str):
            quarters = True
        else:
            quarters = False
    if quarters:
        years = sorted(years, key=quarter_to_datetime)
    else:
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
        # Calculate the percent difference between the two numbers
        percent_diff = abs(prev_value - value) / ((prev_value + value) / 2)

        # Define the acceptable range (in this case, 2%)
        acceptable_range = 0.02

        if value <= prev_value:
            # Check if the percent difference is within the acceptable range
            if percent_diff >= acceptable_range:
                return False

    # If all of the values in the dictionary are increasing, return True
    return True

def get_stock_percentage_change(stock_oject, time):
    history = stock_oject.history(period=time)
    current = history['Close'][-1]
    old = history['Close'][0]
    return (current-old)/old

def get_good_stock_data(stock):
    '''
    returns dictionary(good_stock) or None
    '''
    # for some reason some stocks fail to decode or have garbage values
    try:
        info = stock['data'].info
        if keys_not_missing(info.keys()):
            good_stock = {}
            # Basic info
            good_stock['shortName'] = info['shortName']
            good_stock['industry'] = info['industry']
            good_stock['symbol'] = info['symbol']
            good_stock['exchange'] = stock['exchange']
            good_stock['currentPrice'] = info['currentPrice']
            good_stock['marketCap'] = info['marketCap']
            good_stock['heldPercentInstitutions'] = info['heldPercentInstitutions']

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

            # Assets and debt
            # for some reason they are occationally NA even if the company does have assets or debt
            totalAssets = info.get('totalAssets')
            totalDebt = info.get('totalDebt')
            if totalAssets is None or totalDebt is None:
                good_stock['debtToAssetsRatio'] = 0
            else:
                good_stock['debtToAssetsRatio'] = totalDebt/totalAssets

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
            if large_cap(info['marketCap']) and good_instutional_ownership(info['heldPercentInstitutions']) and affordable_price(info['currentPrice']) and good_pb_ratio(info['priceToBook']) and good_pe_ratio(info['forwardPE']) and good_debt_ratio(good_stock['debtToAssetsRatio']):
                # next earnings date
                # for some reason, the data is not well formatted. 0 or "Value" as keys
                earnings_object = (stock['data'].calendar).to_dict()
                if 0 in earnings_object.keys():
                    nextEarningsDate = (stock['data'].calendar).to_dict()[0]['Earnings Date']
                elif "Value" in earnings_object.keys():
                    nextEarningsDate = (stock['data'].calendar).to_dict()['Value']['Earnings Date']
                good_stock['nextEarningsDate'] = nextEarningsDate

                # Quarterly income
                earnings_info = (stock['data'].get_earnings(freq="quarterly")).to_dict()
                good_stock['4Quarters_increasing_revenue'] = is_increasing(earnings_info['Revenue'])
                good_stock['4Quarters_increasing_profit'] = is_increasing(earnings_info['Revenue'])
                # we only want 4 quarters increasing revenue
                if is_increasing(earnings_info['Revenue']) == False:
                    return None

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
                good_stock['fundamentals_url'] = url
                # stockcharts link with indicators
                url = "https://stockcharts.com/h-sc/ui?s="+info['symbol']+"&p=D&b=5&g=0&id=p69126693727"
                good_stock['technicals_url'] = url
                print(info['symbol']+" stock good")
                return good_stock
            return None
    except:
        return None

def clean_for_csv(good_stocks):
    keys_to_delete = ['sharesOutstanding', 'floatShares', 'debtToEquity', 'returnOnEquity', 'returnOnAssets', 'grossProfits', 'profitMargins', 'totalRevenue', 'debtToAssetsRatio', 'forwardEps', 'trailingEps', 'marketCap', '']
    if isinstance(good_stocks, list):
        for stock in good_stocks:
            for key in keys_to_delete:
                if key in stock:
                    del stock[key]
    else:
        for key in keys_to_delete:
            if key in good_stocks:
                del good_stocks[key]
    return good_stocks

# for testing purposes the following are good stocks:
# ACGL stock good
# ADI stock good
# AEP stock good
# AMAT stock good
# ATVI stock good
# AVGO stock good
# BIDU stock good
# BIIB stock good
def write_symbol_to_csv(symbol, exchange, cache=False):
    ''''''
    start_time = time.time()
    stock = get_symbol_object(symbol, exchange)
    # cache these results
    stock_data_path = general.dataPath(symbol+"_stock_data.pkl")
    if cache:
        stock_data = general.fileLoadCache(stock_data_path)
    else:
        stock_data = []

    if stock_data == []:
        good_stock = get_good_stock_data(stock)
        if good_stock is not None:
            stock_data.append(good_stock)
        general.fileSaveCache(stock_data_path, stock_data)
        print("--- %s seconds to get all stock data  ---" % (round(time.time() - start_time,2)))
    # write to CSV
    if stock_data != []:
        stock_data = clean_for_csv(stock_data)
        stock_csv_path = general.resultsPath(symbol+"_stock_data.csv")
        general.listOfDictsToCSV(stock_data, stock_csv_path)
    else:
        print(symbol+" is not a good stock")
    return stock_data

# 118m to get through NASDAQ
# 165m to get through NYSE
# 283m total
def write_symbols_to_csv(cache=False):
    start_time = time.time()
    stocks = get_all_symbol_object()
    # cache these results
    stock_data_path = general.dataPath("all_stock_data.pkl")
    if cache:
        print (stock_data_path)
        stock_data = general.fileLoadCache(stock_data_path, datestamp=False)
    else:
        stock_data = []

    if stock_data == []:
        for stock in stocks:
            good_stock = get_good_stock_data(stock)
            if good_stock is not None:
                stock_data.append(good_stock)
        general.fileSaveCache(stock_data_path, stock_data)
        print("--- %s seconds to get all stock data  ---" % (round(time.time() - start_time,2)))
    # write to CSV
    if stock_data != []:
        stock_data = clean_for_csv(stock_data)
        stock_csv_path = general.resultsPath("all_stock_data.csv")
        general.listOfDictsToCSV(stock_data, stock_csv_path)
        # write dividend stocks to seperate file
        dividend_symbols = []
        for symbol in stock_data:
            if good_dividend(symbol['dividendYield']):
                dividend_symbols.append(symbol)
        if dividend_symbols != []:
            stock_csv_path = general.resultsPath("dividend_stock_data.csv")
            general.listOfDictsToCSV(dividend_symbols, stock_csv_path)
        else:
            print("No dividend stocks found")
    else:
        print("No good stocks found")
    return stock_data

