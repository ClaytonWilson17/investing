# Determine if you should sell a stock (sell a call) based on technical indicators



# Determine if you should sell a stock (sell a put) based on technical indicators

def sell_based_on_RSI(RSI):
    sell = False
    if float(RSI) > float(65):    
        sell = True
    return (sell)


def sell_based_on_pivot_points(current_price, pivot_resistance_1):
    sell = False
    if float(current_price) >= float(pivot_resistance_1):
        sell = True
    return (sell)


def sell_based_on_keltner_channel(current_price, upper_channel):
    sell = False
    if float(current_price) >= float(upper_channel):
        sell = True
    return (sell)


def sell_based_on_macd(MACD_line, MACD_signal):
    '''
    If the MACD line and signal line cross while they are above the zero line, signal to sell the stock
    '''
    MACD_signal = float(MACD_signal)
    MACD_line = float(MACD_line)
    sell = False
    
    difference = abs(MACD_line - MACD_signal)

    # The value is set to .15 but may need to be changed, i am not sure if the values will ever actually hit 0 exactly
    if (difference < .15) and (MACD_line > 0): 
        sell = True

    return(sell)


def determine_sell_signals(price, RSI=None, pivot_resistance_1=None, upper_keltner_channel=None, macd_line=None, macd_signal=None):

    '''
    All values except price are set to None by default, it will test whatever values you input to see if there is a sell signal on one of the indicators

    Returns True if you should sell the stock and False if there is no sell signal
    '''
    # These variables will be set to true if the technical indicators suggest to sell
    sell_RSI = False
    sell_pivot = False
    sell_kelter = False
    sell_macd = False
    signals_that_are_true = []
    
    if RSI is not None:
        sell_RSI = sell_based_on_RSI(RSI)
        if sell_RSI is True:
            signals_that_are_true.append("RSI")

    if pivot_resistance_1 is not None:
        sell_pivot = sell_based_on_pivot_points(price, pivot_resistance_1)
        if sell_pivot is True:
            signals_that_are_true.append("Resistance1")

    if upper_keltner_channel is not None:
        sell_kelter = sell_based_on_keltner_channel(price, upper_keltner_channel)
        if sell_kelter is True:
            signals_that_are_true.append("Keltner")

    if macd_line is not None and macd_signal is not None:
        sell_macd = sell_based_on_macd(macd_line, macd_signal)
        if sell_macd is True:
            signals_that_are_true.append("MACD")

    if sell_RSI is True or sell_kelter is True or sell_macd is True or sell_pivot is True:
        return ([True, signals_that_are_true])
    else:
        return ([False, ""])

