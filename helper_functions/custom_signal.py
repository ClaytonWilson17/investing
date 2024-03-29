# Determine if you should signal a stock based on our own custom settings

from helper_functions import general

def support_resistance(current_price, support_price_1, resistance_price_1):
    signal = None
    if float(current_price) <= float(support_price_1):
        signal = 'buy'
    elif float(current_price) >= float(resistance_price_1):
        signal = 'sell'
    else:
        signal = 'none'
        
    return (signal)



def markus_signal(rsi, stochastic, macd_line, signal_line):
    signal = 'none'

    # decide if there is a buy signal
    if float(rsi) > float(50): 
        if float(stochastic) > float(50):
            if macd_line > signal_line and macd_line < float(0):
                signal = 'buy'

    # decide if there is a sell signal
    if float(rsi) < float(50):
        if float(stochastic) < float(50):
            if macd_line < signal_line and macd_line > float(0):
                signal = 'sell'

    return (signal)



def determine_signals(technical_stock_data):
    '''
    input:
    The output from the get_technical_indicators function

    output:
    the paths to the csv files generated
    '''
    logger = general.getCustomLogger("log.txt")
    stocks_with_buy_signal = []
    stocks_with_sell_signal = []


    for stock in technical_stock_data:
        print("Determining buy/sell for symbol: " + str(stock['Symbol']))
        logger.debug("Determining buy/sell for symbol: " + str(stock['Symbol']))

        markus_result = markus_signal(stock['RSI'], stock['Stochastic'], stock['MACD_line'], stock['MACD_signal'])
        support_resistance_result = support_resistance(stock['Price'], stock['Pivot support 1'], stock['Pivot resistance 1'])

        new_dict = {}
        new_dict['Symbol'] = stock['Symbol']
        new_dict['Price'] = stock['Price']
        new_dict['Signal'] = 'none'
        #new_dict['daily_chart'] = "https://stockcharts.com/h-sc/ui?s="+stock['Symbol']+"&p=D&yr=0&mn=1&dy=0&id=p00835703143"
        #new_dict['5mo_chart'] = "https://stockcharts.com/h-sc/ui?s="+stock['Symbol']+"&p=D&b=5&g=0&id=p05555723250"

        if markus_result == 'buy':
            new_dict['Signal'] = 'Markus Buy Signal'
        if support_resistance_result == 'buy':
            new_dict['Signal'] = 'S&R Buy Signal'

        if markus_result == 'sell':
            new_dict['Signal'] = 'Markus Sell Signal'
        if support_resistance_result == 'sell':
            new_dict['Signal'] = 'S&R Sell Signal'
        
        if new_dict['Signal'] == 'Markus Buy Signal' or new_dict['Signal'] == 'S&R Buy Signal':
            stocks_with_buy_signal.append(new_dict)

        if new_dict['Signal'] == 'Markus Sell Signal' or new_dict['Signal'] == 'S&R Sell Signal':
            stocks_with_sell_signal.append(new_dict)

    # add fundamental data back in 
    print("Getting the most recent fundamentals to add the fundamental columns to stocks with buy/sell signal...")
    logger.debug("Getting the most recent fundamentals to add the fundamental columns to stocks with buy/sell signal...")
    fundamentals = general.get_most_recent_fundamentals()
    for stock in stocks_with_buy_signal:
        for fund in fundamentals:
            if stock['Symbol'] == fund['symbol']:
                stock.update(fund)
    fundamentals = general.get_most_recent_fundamentals()
    for stock in stocks_with_sell_signal:
        for fund in fundamentals:
            if stock['Symbol'] == fund['symbol']:
                stock.update(fund)

    result_paths = []    
    
    if stocks_with_buy_signal:
        buy_path = general.resultsPath('Buy Signals.csv')
        general.listOfDictsToCSV(stocks_with_buy_signal, buy_path)
        result_paths.append(buy_path)

    if stocks_with_sell_signal:
        sell_path = general.resultsPath('Sell Signals.csv')
        general.listOfDictsToCSV(stocks_with_sell_signal, sell_path)
        result_paths.append(sell_path)

    if result_paths:
        return result_paths
    else:
        return 'none'
    

        
        
        


        