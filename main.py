# Main file which controls all of the inputs to the functions

from helper_functions import custom_signal, get_technical_indicators, general, send_email, get_fundamental_indicators
import os
import sys
from datetime import datetime, date
import argparse

# Get argument
parser = argparse.ArgumentParser()
parser.add_argument("--technical_only", action="store_true")
parser.add_argument("--stored_data", action="store_true")
args = parser.parse_args()


# delete previous log file and create a new blank file
if not os.path.exists("data"):
    os.makedirs("data")
log_path = general.dataPath('log.txt')
if os.path.exists(log_path):
    with open(log_path, 'w'):
        pass
    os.remove(log_path)
    print(f'{log_path} has been deleted.')
else:
    print(f'{log_path} does not exist.')
with open(log_path, 'w'):
    pass

logger = general.getCustomLogger("log.txt")

today = datetime.now()
today = today.strftime("%m/%d/%y %H:%M")
print("starting this script on: "+today)
logger.debug("starting this script on: "+today)

# List of stocks to get technical indicator data on
#NASDAQ_symbols = ['CSX', 'AMD', 'GOOGL', 'AMZN', 'DBX', 'AAPL', 'SBUX', 'MSFT', 'CSCO', 'TSCO', 'NVDA']
#NYSE_symbols = ['BAC', 'SYF', 'IBM', 'DKS', 'KR', 'UNH', 'DUK', 'TM', 'CNI', 'V', 'DE', 'FE', 'MA', 'O', 'LMT', 'WMT', 'DGX', 'WM', 'GIS', 'JPM', 'T', 'ABBV', 'JNJ', 'VALE', 'LOW', 'LEN', 'CVX', 'XOM', 'CAT', 'NKE']
NASDAQ_symbols = []
NYSE_symbols = [] 
added_stocks = [{'symbol': "AEP", 'exchange': "NASDAQ"},{'symbol': "CME", 'exchange': "NASDAQ"},
                {'symbol': "AFL", 'exchange': "NYSE"},{'symbol': "CAT", 'exchange': "NYSE"},
                {'symbol': "V", 'exchange': "NYSE"},{'symbol': "JNJ", 'exchange': "NYSE"},
                {'symbol': "DUK", 'exchange': "NYSE"}]
blacklisted = []


# Get fundamental analysis symbols and data if the command line arg 'technical_only' doesnt specify otherwise
recent_fundamentals = []

if args.technical_only:
    logger.debug("You have selected to run this script in technical_only mode")
    if args.stored_data:
        recent_fundamentals = general.CSVToListOfDicts(general.static_path("all_stock_data.csv"))
    else:
        recent_fundamentals = general.get_most_recent_fundamentals()
    recent_fundamentals = recent_fundamentals + added_stocks
    for dict in recent_fundamentals:
        if 'exchange' not in dict.keys():
            dict['exchange'] = 'None'

        if dict['exchange'] == "NYSE":
            if dict['symbol'] not in NYSE_symbols:
                NYSE_symbols.append(dict['symbol'])
        if dict['exchange'] == "NASDAQ":
            if dict['symbol'] not in NASDAQ_symbols:
                NASDAQ_symbols.append(dict['symbol'])

else:
    print("Getting Fundamental analysis symbols and data...\n")
    logger.debug("Getting Fundamental analysis symbols and data...")
    list_of_dicts = get_fundamental_indicators.write_symbols_to_csv(added_tickers=added_stocks,blacklisted_tickers=blacklisted, cache=False)
    for dict in list_of_dicts:
        if dict['exchange'] == "NYSE":
            if dict['symbol'] not in NYSE_symbols:
                NYSE_symbols.append(dict['symbol'])
        if dict['exchange'] == "NASDAQ":
            if dict['symbol'] not in NASDAQ_symbols:
                NASDAQ_symbols.append(dict['symbol'])

# Get technical indicators for all stocks
print("Getting technical analysis data...\n")
logger.debug("Getting technical analysis data...")
technical_data = []
technical_data = get_technical_indicators.get_tech_indicators(NYSE_symbols=NYSE_symbols, NASDAQ_symbols=NASDAQ_symbols)


# run the signal analysis on all technical indicator data
print("Running analysis on technical indicators to find buy/sell signals...\n")
logger.debug("Running analysis on technical indicators to find buy/sell signals...")
temp = custom_signal.determine_signals(technical_data)
if temp != 'none':
    files = temp

today = datetime.now()
today = today.strftime("%m/%d/%y %H:%M")
print("Done with fundamental and technical analysis on: "+today)
logger.debug("Done with fundamental and technical analysis on: "+today)

# get the list of all stocks and their data and turn it into csv so it can be emailed out
if not args.technical_only:
    all_stock_data = general.find_recent_file('all_stock_data')
    list_of_dicts = general.fileLoadCache(all_stock_data ,datestamp=False)
    result_path = general.resultsPath('all_stock_data')
    all_stock_data = general.listOfDictsToCSV(list_of_dicts, result_path)
    files.append(result_path + '.csv')

# Email out the files
general.get_env_vars()
subject = "Stock signals for the day " + str(datetime.today().strftime('%Y-%m-%d'))


body = """Hello humans, please see the attached csv files for the current buy and sell signals for the day...  buy (sell a put)  sell (sell a call)\n\n
We analyze stocks every day. We monitor their changes. If a stock is removed, you should probably stop investing in it because it no longer meets our criteria.\n"""

# Get which stocks were added or removed from our list of good stocks
if not args.technical_only:
    deltas = get_fundamental_indicators.get_delta()
    body = body + "Added stocks: "+','.join(deltas['added'])+"\n"
    body = body + "Removed stocks: "+','.join(deltas['removed'])+"\n"

receiver_emails = []
receiver_emails.append(os.environ['simon_email'])
receiver_emails.append(os.environ['clayton_email'])

print("Send out emails with any files generated attached\n")
logger.debug("Send out emails with any files generated attached")
log_path = general.dataPath('log.txt')
files.append(log_path)

for reciever in receiver_emails:
    send_email.send_email(subject=subject, body=body, receiver_email=reciever, files=files)
    None