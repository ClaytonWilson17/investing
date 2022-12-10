# Main file which controls all of the inputs to the functions

from helper_functions import get_technical_indicators, output_to_csv, sell_signal, buy_signal

# List of stocks to get technical indicator data on
NASDAQ_symbols = ['CSX', 'AMD', 'GOOGL', 'AMZN', 'DBX', 'AAPL', 'SBUX', 'MSFT', 'CSCO', 'TSCO', 'NVDA']
NYSE_symbols = ['BAC', 'SYF', 'IBM', 'DKS', 'KR', 'UNH', 'DUK', 'TM', 'CNI', 'V', 'DE', 'FE', 'MA', 'O', 'LMT', 'WMT', 'DGX', 'WM', 'GIS', 'JPM', 'T', 'ABBV', 'JNJ', 'VALE', 'LOW', 'LEN', 'CVX', 'XOM', 'CAT', 'NKE']

technical_data = []
technical_data =get_technical_indicators.get_tech_indicators(NYSE_symbols=NYSE_symbols, NASDAQ_symbols=NASDAQ_symbols)
# Returns the following keys: Symbol, Price, RSI, Pivot middle, Pivot support 1, Pivot support 2, MACD_line, MACD_signal

buy_indicators = []
stocks_to_buy = []

for data in technical_data:
    signal = buy_signal.determine_buy_signals(data['Price'], data['RSI'], data['Pivot support 1'], data['Pivot support 1'], data['MACD_line'], data['MACD_signal'])
    if signal == True:
        stocks_to_buy.append(data['Symbol'])

print (stocks_to_buy)
#output_to_csv.print_to_csv(technical_data, 'testing')

