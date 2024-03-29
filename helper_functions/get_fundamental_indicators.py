# retrieves all of the technical indicators needed to determine buy and sell signals
exec("""\nimport sys,os\nexec(\"\"\"\\ndef get_git_root(path=os.getcwd(),display=False):\\n    \\n    '''\\n    Get Git Root Directory. Only recursively goes up 10 directories.\\n    RETURNS: None or absolute path to git root directory\\n    '''\\n    count = 0\\n    prefix = ""\\n    while count < 10:\\n        if os.path.exists(prefix+'.git'):\\n            return os.path.abspath(prefix)\\n        else:\\n            prefix +="../"\\n            count+=1\\n    print("No git top level directory")\\n    return None\\n\"\"\")\ngitroot=get_git_root()\nsys.path.append(os.path.abspath(gitroot))\n""") # one liner statement that adds the root of this repo to python for inports
from helper_functions import general
from importlib import reload
reload(general)

import os
import json
import requests
from pathlib import Path
import time
from datetime import date, datetime, timedelta
import pandas as pd
import yfinance as yf #https://github.com/ranaroussi/yfinance
from datetime import datetime

logger = general.getCustomLogger("log.txt")

def is_composite_stock(stock_info, symbol):
    try:
        for comp_symbol in ["^IXIC", "IXIC", "^NYA", "NYA", "^DJI", "DJI", "^SPX", "SPX"]:
            if comp_symbol == symbol:
                return True
    except:
        return False
    return False

def get_composite_stock_symbols(stock_info, symbol):
    # For yahoo finance tool
        # nasdaq = ^IXIC
        # NYSE = ^NYA
        # Dow  = ^DJI 
        # SP500 = ^SPX
    # For google finance:
        # nasdaq = .IXIC:INDEXNASDAQ
        # NYA = NYA:INDEXNYSEGIS
        # DOW = .DJI:INDEXDJX
        # SP500 = .INX:INDEXSP
    # For stockcharts: 
        # nasdaq = %24COMPQ
        # NYA = %24NYA
        # DOW = %24INDU
        # SP500 = %24SPCMI
    if symbol == "^IXIC":
        stock_info['goog_finance_symbol'] = ".IXIC:INDEXNASDAQ"
        stock_info['stockcharts_syymbol'] = "%24COMPQ"
        stock_info['comp_symbol'] = "IXIC"
        stock_info['exchange'] = "NASDAQ"
    elif symbol == "^NYA":
        stock_info['goog_finance_symbol'] = "NYA:INDEXNYSEGIS"
        stock_info['stockcharts_syymbol'] = "%24NYA"
        stock_info['comp_symbol'] = "NYA"
        stock_info['exchange'] = "NYSE"
    return stock_info

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
    logger.debug("There are a total of: "+str(len(symbols))+" symbols")
    return symbols

# this downloads symbol data for the past:
#  symbol "info" takes 3 seconds to download. 9.3 hours total
#  symbol (% changes last 5 years, 4 quarters earnings info) takes 1.7 sec
# For yahoo finance tool
    # nasdaq = ^IXIC
    # NYSE = ^NYA
    # Dow  = ^DJI 
    # SP500 = ^SPX
def get_all_symbol_object(add_composites=False, blacklist=[]):
    ticker_list = get_all_symbols()
    if add_composites:
        ticker_list.append({'Code': "^IXIC", 'Exchange': "NASDAQ"})
        ticker_list.append({'Code': "^NYA", 'Exchange': "NYSE"})

    stock_data = []
    for ticker in ticker_list:
        if {"symbol": ticker['Code'], "exchange": ticker['Exchange']} not in blacklist:
            data = yf.Ticker(ticker['Code'])
            stock_data.append({"symbol": ticker['Code'],"data":data, "exchange":ticker['Exchange']})
    return stock_data

def get_symbol_object(stock_code, exchange):
    data = yf.Ticker(stock_code)
    stock_data = {"symbol": stock_code, "data":data, "exchange":exchange}
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
    if float(dividend) > .01: #2%
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
    required_keys = ['shortName', 'bid', 'forwardEps', 'trailingEps', 'forwardPE',
     'trailingPE', 'priceToBook', 'profitMargins', 'totalRevenue', 'grossProfits', 'returnOnAssets', 'returnOnEquity', 
     'debtToEquity', 'sharesOutstanding', 'floatShares']   
    if set(required_keys).issubset(set(keys)):
        return True
    else:
        #uncomment for troubleshooting
        #missing_keys = set(required_keys) - set(keys)
        #print("The following keys are missing:", missing_keys)
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

def increasing_revenue(earnings_info):
    if is_increasing(earnings_info['Revenue']):
        return True
    else:
        return False

def increasing_income(earnings_info):
    if is_increasing(earnings_info['Earnings']):
        return True
    else:
        return False

def replace_none_values(object, list_of_keys):
    for key in list_of_keys:
        if key not in object.keys():
            object[key] = 0
        elif object[key] is None:
            object[key] = 0
    return object

def get_good_stock_data(stock, get_any_stock=False):
    '''
    returns dictionary(good_stock) or None
    '''
    # for some reason some stocks fail to decode or have garbage values
    try:
        good_stock = {}
        info = stock['data'].info
        fast_info = stock['data'].fast_info
        symbol = stock['symbol']
        
        if info is None:
            return None
        
        if is_composite_stock(info, symbol):
            info = get_composite_stock_symbols(info, symbol)
            #good_stock['currentPrice'] = fast_info['regularMarketPrice']
        
        if keys_not_missing(info.keys()) or is_composite_stock(info, symbol):
            # go through each of the following keys
            info = replace_none_values(info, ['heldPercentInstitutions', 'industry', 'profitMargins','dividendYield', 'forwardEps', 'trailingEps', 'forwardPE', 'trailingPE', 'priceToBook', 'returnOnAssets', 'returnOnEquity', 'debtToEquity', 'sharesOutstanding', 'floatShares', 'totalRevenue', 'grossProfits'])
            
            # Basic info
            good_stock['shortName'] = info['shortName']
            good_stock['industry'] = info['industry']
            good_stock['symbol'] = symbol
            if is_composite_stock(info, symbol):
                good_stock['symbol'] = info['comp_symbol']
            good_stock['exchange'] = stock['exchange']
            good_stock['currentPrice'] = fast_info['last_price']
            good_stock['marketCap'] = fast_info['market_cap']
        
            good_stock['heldPercentInstitutions'] = round((info['heldPercentInstitutions']*100),2)
            # Dividends
            good_stock['dividendYield'] = (info['dividendYield']*100) #0.0272=2.72%
            
            exDividendDate = info['exDividendDate']
            if exDividendDate is not None:
                from datetime import datetime
                good_stock['exDividendDate'] = datetime.utcfromtimestamp(int(exDividendDate)).strftime('%c')
            else:
                good_stock['exDividendDate'] = None
            
            # EPS
            good_stock['forwardEps'] = round(info['forwardEps'],2)
            good_stock['trailingEps'] = round(info['trailingEps'],2)
            # P/E ratio
            good_stock['forwardPE'] = round(info['forwardPE'],2)
            good_stock['trailingPE'] = round(info['trailingPE'],2)
            # P/B ratio
            good_stock['priceToBook'] = round(info['priceToBook'],2)

            # Assets and debt
            # for some reason they are occationally NA even if the company does have assets or debt
            # totalAssets = info.get('totalAssets')
            # totalDebt = info.get('totalDebt')
            # if totalAssets is None or totalDebt is None:
            #     good_stock['debtToAssetsRatio'] = 0
            # else:
            #     good_stock['debtToAssetsRatio'] = totalDebt/totalAssets

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
            great_stock = False
            if (large_cap(good_stock['marketCap']) and good_dividend(info['dividendYield']) and good_instutional_ownership(info['heldPercentInstitutions']) and affordable_price(good_stock['currentPrice']) and good_pb_ratio(info['priceToBook']) and good_pe_ratio(info['forwardPE'])):
                great_stock = True
            if get_any_stock or great_stock or is_composite_stock(info, symbol):
                # Composite stocks (SP500, DOW jones, etc) don't have earnings
                if is_composite_stock(info, symbol):
                    good_stock['nextEarningsDate'] = "NA"
                    good_stock['4Quarters_increasing_revenue'] = "NA"
                    good_stock['4Quarters_increasing_profit'] = "NA"
                    good_stock['4years_increasing_revenue'] = "NA"
                    good_stock['4years_increasing_profit'] = "NA"
                else:
                    # next earnings date
                    # for some reason, the data is not well formatted. 0 or "Value" as keys
                    earnings_object = (stock['data'].calendar).to_dict()
                    if 0 in earnings_object.keys():
                        nextEarningsDate = (stock['data'].calendar).to_dict()[0]['Earnings Date']
                    elif "Value" in earnings_object.keys():
                        nextEarningsDate = (stock['data'].calendar).to_dict()['Value']['Earnings Date']
                    good_stock['nextEarningsDate'] = nextEarningsDate

                    # Quarterly/Yearly income
                    quarterly_earnings_info = (stock['data'].get_earnings(freq="quarterly")).to_dict()
                    yearly_earnings_info = (stock['data'].get_earnings(freq="yearly")).to_dict()
                    good_stock['4Quarters_increasing_revenue'] = increasing_revenue(quarterly_earnings_info)
                    good_stock['4Quarters_increasing_profit'] = increasing_income(quarterly_earnings_info)
                    good_stock['4years_increasing_revenue'] = increasing_revenue(yearly_earnings_info)
                    good_stock['4years_increasing_profit'] = increasing_income(yearly_earnings_info)

                    # we only want 4 quarters increasing revenue or last 4 years increasing revenue/income
                    if is_composite_stock(info, symbol) or ((get_any_stock == False) and not (good_stock['4Quarters_increasing_revenue'] or (good_stock['4years_increasing_revenue'] and good_stock['4years_increasing_profit']))):
                        print(symbol+" is a good stock but has a bad income report. Skipping...")
                        logger.debug(symbol+" is a good stock but has a bad income report. Skipping...")
                        return None
                    
                # Changes last: 1 week, 1 month, 3 months, 6 months, 1 year, 5 year
                good_stock['pct_chg_5y'] = round((get_stock_percentage_change(stock['data'], "5y")*100),2)
                good_stock['pct_chg_1y'] = round((get_stock_percentage_change(stock['data'], "1y")*100),2)
                good_stock['pct_chg_6mo'] = round((get_stock_percentage_change(stock['data'], "6mo")*100),2)
                good_stock['pct_chg_3mo'] = round((get_stock_percentage_change(stock['data'], "3mo")*100),2)
                good_stock['pct_chg_1mo'] = round((get_stock_percentage_change(stock['data'], "1mo")*100),2)
                good_stock['pct_chg_1wk'] = round((get_stock_percentage_change(stock['data'], "1wk")*100),2)
                
                # special consideration is needed for indexes when building URLs
                if is_composite_stock(info, symbol):
                    # Google finance link
                    url = "https://g.co/finance/"+info['goog_finance_symbol']
                    good_stock['fundamentals_url'] = url
                    # stockcharts link with indicators
                    url = "https://stockcharts.com/h-sc/ui?s="+info['stockcharts_syymbol']+"&p=D&yr=0&mn=1&dy=0&id=p00835703143"
                    good_stock['daily_chart'] = url
                    url = "https://stockcharts.com/h-sc/ui?s="+info['stockcharts_syymbol']+"&p=D&b=5&g=0&id=p05555723250"
                    good_stock['5mo_chart'] = url
                else:
                    # Google finance link
                    url = "https://g.co/finance/"+symbol+":"+stock['exchange']
                    good_stock['fundamentals_url'] = url
                    # stockcharts link with indicators
                    url = "https://stockcharts.com/h-sc/ui?s="+symbol+"&p=D&yr=0&mn=1&dy=0&id=p00835703143"
                    good_stock['daily_chart'] = url
                    url = "https://stockcharts.com/h-sc/ui?s="+symbol+"&p=D&b=5&g=0&id=p05555723250"
                    good_stock['5mo_chart'] = url

                if great_stock:
                    print(symbol+" stock good")
                    logger.debug(symbol+" stock good")
                else:
                    print(symbol+" was a bad stock but returning results anyway")
                    logger.debug(symbol+" was a bad stock but returning results anyway")
                return good_stock
            return None
    except Exception as e:
        return None

# this function is because we don't want to see all of the keys in excel
# we just want the most important details about the stock
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
def write_symbol_to_csv(symbol, exchange, cache=False, get_any_stock=False):
    ''''''
    stock = get_symbol_object(symbol, exchange)
    # cache these results
    stock_data_path = general.dataPath(symbol+"_stock_data.pkl")
    if cache:
        stock_data = general.fileLoadCache(stock_data_path)
    else:
        stock_data = None

    # generate new data
    if stock_data is None:
        stock_data = get_good_stock_data(stock, get_any_stock=get_any_stock)
        if stock_data is not None:
            stock_data = clean_for_csv(stock_data)
            stock_csv_path = general.resultsPath(symbol+"_stock_data.csv")
            general.listOfDictsToCSV([stock_data], stock_csv_path)
        else:
            print(symbol+" is not a good stock")
            logger.debug(symbol+" is not a good stock")
        general.fileSaveCache(stock_data_path, stock_data)
        return stock_data
    # use cached data
    else:
        return stock_data

# 118m to get through NASDAQ
# 165m to get through NYSE
# 283m total
def write_symbols_to_csv(added_tickers=[],blacklisted_tickers=[],do_all_tickers=True,cache=False):
    '''
    format for added tickers is:
    [{'symbol': "GOOG", 'exchange': "NASDAQ"}, ...]

    format for blacklisted tickers is:
    [{'symbol': "GOOG", 'exchange': "NASDAQ"}, ...]
    '''
    start_time = time.time()
    stocks = []
    if do_all_tickers:
        stocks = get_all_symbol_object(blacklist=blacklisted_tickers)
    added_ticker_objects = []
    for ticker in added_tickers:
        object = get_symbol_object(ticker['symbol'],ticker['exchange'])
        if ticker not in blacklisted_tickers:
            stocks.append(object)
            added_ticker_objects.append(object)
        else:
            if object in stocks:
                stocks.remove(object)

    # cache these results
    stock_data_path = general.dataPath("all_stock_data.pkl")
    if cache:
        stock_data = general.fileLoadCache(stock_data_path, datestamp=True)
    else:
        stock_data = None

    if stock_data is None:
        print("Starting download of stock data... this should take about 4-6 hours.")
        logger.debug("Starting download of stock data... this should take about 4-6 hours.")
        count = 0
        percent_increment = 100 / len(stocks)
        
        stock_data = []
        for stock in stocks:
            count+=1
            progress = (count + 1) * percent_increment
            # Print the progress every 100 elements
            if count % 1000 == 0:
                print(f'{progress}% complete')
                logger.debug(f'{progress}% complete')
            # get stock data
            if stock in added_ticker_objects:
                good_stock = get_good_stock_data(stock, get_any_stock=True)
            else:
                good_stock = get_good_stock_data(stock)
            if good_stock is not None:
                stock_data.append(good_stock)
        general.fileSaveCache(stock_data_path, stock_data)
        print("--- %s seconds to get all stock data  ---" % (round(time.time() - start_time,2)))
        logger.debug("--- %s seconds to get all stock data  ---" % (round(time.time() - start_time,2)))
    # write to CSV
    if stock_data != []:
        stock_data = clean_for_csv(stock_data)
        stock_csv_path = general.resultsPath("all_stock_data.csv")
        general.listOfDictsToCSV(stock_data, stock_csv_path)
    else:
        print("No good stocks found")
        logger.debug("No good stocks found")
    return stock_data


def get_delta():
    try:
        filename = "all_stock_data"
        today = filename+str(date.today())+".pkl"
        today_path = general.dataPath(today)
        today_stocks = general.fileLoadCache(today_path, datestamp=False)

        # attempt to get yesterday's stock file if it exists, otherwise keep going back to the day before
        days_ago = 1
        today = datetime.now() 
        file_does_not_exist = True
        while file_does_not_exist == True:
            if days_ago > 60:
                print ("There is no past fundamental data so the Markus/Chuck signal will not work")
                logger.debug("There is no past fundamental data so the Markus/Chuck signal will not work")
                return 'no data'
            past_date = today - timedelta(days=days_ago)
            past_date = past_date.strftime('%Y-%m-%d')
            yesterday_path = general.dataPath("all_stock_data" + str(past_date) + ".pkl")
            my_file = Path(yesterday_path)
            if my_file.is_file():
                file_does_not_exist = False
            else:
                print ("There is no past for: " + str(past_date) + ". Going back one more day")
                logger.debug("There is no past for: " + str(past_date) + ". Going back one more day")
                days_ago = days_ago + 1
        yesterday_stocks = general.fileLoadCache(yesterday_path, datestamp=False)

        today_symbols = [stock['symbol'] for stock in today_stocks]
        yesterday_symbols = [stock['symbol'] for stock in yesterday_stocks]
        removed_stocks = [d['symbol'] for d in yesterday_stocks if d['symbol'] not in today_symbols]
        added_stocks = [d['symbol'] for d in today_stocks if d['symbol'] not in yesterday_symbols]
        
        yesterday_csv = general.resultsPath("previous_stocks.csv")
        today_csv = general.resultsPath("today_stocks.csv")
        general.listOfDictsToCSV(yesterday_stocks, yesterday_csv)
        general.listOfDictsToCSV(today_stocks, today_csv)
    except:
        removed_stocks = []
        added_stocks =[]

    return {"added": added_stocks, "removed": removed_stocks}