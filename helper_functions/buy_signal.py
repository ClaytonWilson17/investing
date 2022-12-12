# Determine if you should buy a stock (sell a put) based on technical indicators

def buy_based_on_RSI(RSI):
    buy = False
    if float(RSI) < float(31):    
        buy = True
    return (buy)


def buy_based_on_pivot_points(current_price, support_price_1):
    buy = False
    if float(current_price) <= float(support_price_1):
        buy = True
    return (buy)


def buy_based_on_keltner_channel(current_price, bottom_channel):
    buy = False
    if float(current_price) <= float(bottom_channel):
        buy = True
    return (buy)


def buy_based_on_macd(MACD_line, MACD_signal):
    '''
    If the MACD line and signal line cross while they are below the zero line, signal to buy the stock
    '''
    MACD_signal = float(MACD_signal)
    MACD_line = float(MACD_line)
    buy = False
    
    difference = abs(MACD_line - MACD_signal)

    # The value is set to .15 but may need to be changed, i am not sure if the values will ever actually hit 0 exactly
    if (difference < .15) and (MACD_line < 0): 
        buy = True

    return(buy)


def determine_buy_signals(price, RSI=None, pivot_support_1=None, lower_keltner_channel=None, macd_line=None, macd_signal=None):

    '''
    All values except price are set to None by default, it will test whatever values you input to see if there is a buy signal on one of the indicators

    Returns True if you should buy the stock and False if there is no buy signal
    '''
    # These variables will be set to true if the technical indicators suggest to buy
    buy_RSI = False
    buy_pivot = False
    buy_kelter = False
    buy_macd = False
    signals_that_are_true = []
    
    if RSI is not None:
        buy_RSI = buy_based_on_RSI(RSI)
        signals_that_are_true.append("RSI")
    if pivot_support_1 is not None:
        buy_pivot = buy_based_on_pivot_points(price, pivot_support_1)
        signals_that_are_true.append("Support1")
    if lower_keltner_channel is not None:
        buy_kelter = buy_based_on_keltner_channel(price, lower_keltner_channel)
        signals_that_are_true.append("Keltner")
    if macd_line is not None and macd_signal is not None:
        buy_macd = buy_based_on_macd(macd_line, macd_signal)
        signals_that_are_true.append("MACD")

    if buy_RSI is True or buy_kelter is True or buy_macd is True or buy_pivot is True:
        return ([True, signals_that_are_true])
    else:
        return ([False, ""])