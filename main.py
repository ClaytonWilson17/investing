# Main file which controls all of the inputs to the functions

from helper_functions import custom_signal, get_technical_indicators, sell_signal, general, send_email, get_fundamental_indicators, markus_signal
import os

# List of stocks to get technical indicator data on
#NASDAQ_symbols = ['CSX', 'AMD', 'GOOGL', 'AMZN', 'DBX', 'AAPL', 'SBUX', 'MSFT', 'CSCO', 'TSCO', 'NVDA']
#NYSE_symbols = ['BAC', 'SYF', 'IBM', 'DKS', 'KR', 'UNH', 'DUK', 'TM', 'CNI', 'V', 'DE', 'FE', 'MA', 'O', 'LMT', 'WMT', 'DGX', 'WM', 'GIS', 'JPM', 'T', 'ABBV', 'JNJ', 'VALE', 'LOW', 'LEN', 'CVX', 'XOM', 'CAT', 'NKE']
NASDAQ_symbols = []
NYSE_symbols = []

# Get fundamental analysis symbols and data
list_of_dicts = get_fundamental_indicators.write_symbols_to_csv(cache=True)
for dict in list_of_dicts:
    if dict['exchange'] == "NYSE":
        if dict['symbol'] not in NYSE_symbols:
            NYSE_symbols.append(dict['symbol'])
    if dict['exchange'] == "NASDAQ":
        if dict['symbol'] not in NASDAQ_symbols:
            NASDAQ_symbols.append(dict['symbol'])

# Get technical indicators for all stocks
technical_data = []
technical_data =get_technical_indicators.get_tech_indicators(NYSE_symbols=NYSE_symbols, NASDAQ_symbols=NASDAQ_symbols)
# Returns the following keys: Symbol, Price, RSI, Pivot middle, Pivot support 1, Pivot support 2, MACD_line, MACD_signal, Keltner lower, Keltner upper

# Store indicators to be used as a reference in the future:
data_path = general.dataPath("historical_indicators.pkl")
general.fileSaveCache(data_path, technical_data, datestamp=True)

historical_indicators = general.fileLoadCache(data_path)


'''

# Find stocks based on custom signal
stocks_to_buy = []
for data in technical_data:
    signal = custom_signal.determine_signals(data['Price'], data['RSI'], data['Pivot support 1'], data['Keltner lower'])
    if signal[0] == 'buy':
        data['Based on Indicators'] = signal[1]
        data['Signal'] = signal[0]
        stocks_to_buy.append(data)
    else:
        print (str(data['Symbol']) + " did not pass the Custom signal")
custom_stocks_to_buy = general.clean_list_of_dicts(stocks_to_buy)

for stocks in custom_stocks_to_buy:
    for fundamental_data in list_of_dicts:
        if stocks['Symbol'] == fundamental_data['symbol']:
            stocks.update(fundamental_data)

custom_path = general.resultsPath('Custom Signal.csv')
if len(custom_stocks_to_buy) > 0:
    general.listOfDictsToCSV(custom_stocks_to_buy, custom_path)
'''







# Find stocks based on Markus signal
stocks_to_buy = []
stocks_to_sell = []
for data in technical_data:
    past_data = general.get_historical_indicators(sym=data['Symbol'], days_ago=1)
    if past_data != 'no data':
        signal = []
        signal = markus_signal.determine_buy_signals(RSI=data['RSI'], past_RSI=past_data['RSI'], stochastic=data['Stochastic'], past_stochastic=past_data['Stochastic'] ,macd_line=data['MACD_line'], macd_signal=data['MACD_signal'])
        if signal[0] == 'buy':
            print (signal)
            data['Based on Indicators'] = signal[1]
            data['Signal'] = signal[0]
            stocks_to_buy.append(data)
        signal = markus_signal.determine_sell_signals(RSI=data['RSI'], past_RSI=past_data['RSI'], stochastic=data['Stochastic'], past_stochastic=past_data['Stochastic'] ,macd_line=data['MACD_line'], macd_signal=data['MACD_signal'])
        if signal[0] == 'sell':
            data['Based on Indicators'] = signal[1]
            data['Signal'] = signal[0]
            stocks_to_sell.append(data)


markus_stocks_to_buy = general.clean_list_of_dicts(stocks_to_buy)
markus_stocks_to_sell = general.clean_list_of_dicts(stocks_to_sell)

# Add fundamental analysis data back to dictionary
for stocks in markus_stocks_to_buy:
    for fundamental_data in list_of_dicts:
        if stocks['Symbol'] == fundamental_data['symbol']:
            stocks.update(fundamental_data)
for stocks in markus_stocks_to_sell:
    for fundamental_data in list_of_dicts:
        if stocks['Symbol'] == fundamental_data['symbol']:
            stocks.update(fundamental_data)


# Output results from markus indicator to csv and store the file path to email later
files = []

markus_buy_path = general.resultsPath('Markus Buy Signal.csv')
if len(markus_stocks_to_buy) > 0:
    files.append(markus_buy_path)
    general.listOfDictsToCSV(markus_stocks_to_buy, markus_buy_path)
markus_sell_path = general.resultsPath('Markus Sell Signal.csv')
if len(markus_stocks_to_sell) > 0:
    files.append(markus_sell_path)
    general.listOfDictsToCSV(markus_stocks_to_sell, markus_sell_path)



#allpath = general.resultsPath('All Stocks.csv')
#general.listOfDictsToCSV(technical_data, allpath)



# Email out the files
general.get_env_vars()
subject = "Stock signals for the day"
body = "Hello humans, please see the attached csv files for the current buy and sell signals for the day...  buy (sell a put)  sell (sell a call)"
receiver_emails = []
receiver_emails.append(os.environ['simon_email'])
receiver_emails.append(os.environ['clayton_email'])

for reciever in receiver_emails:
    send_email.send_email(subject=subject, body=body, receiver_email=reciever, files=files)

