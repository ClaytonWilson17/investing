# Determine if you should signal a stock (sell a put) based on technical indicators

def based_on_RSI(RSI):
    signal = None
    if float(RSI) <= float(35):    
        signal = 'buy'
    return (signal)


def based_on_pivot_points(current_price, support_price_1):
    signal = None
    if float(current_price) <= float(support_price_1):
        signal = 'buy'
    return (signal)


def based_on_keltner_channel(current_price, bottom_channel):
    signal = None
    if float(current_price) <= float(bottom_channel):
        signal = 'buy'
    return (signal)


def based_on_macd(MACD_line, MACD_signal):
    '''
    If the MACD line and signal line cross while they are below the zero line, signal = buy
    '''
    MACD_signal = float(MACD_signal)
    MACD_line = float(MACD_line)
    signal = None
    
    difference = (MACD_line - MACD_signal)
    

    # The value is set to .2 but may need to be changed, i am not sure if the values will ever actually hit 0 exactly
    if (difference >= 0 ) and (difference < .2) and (MACD_line < 0): 
        signal = None

    return(signal)


def determine_signals(price, RSI=None, pivot_support_1=None, lower_keltner_channel=None, macd_line=None, macd_signal=None):

    '''
    All values except price are set to None by default, it will test whatever values you input to see if there is a signal signal on one of the indicators

    Returns 'buy' if you should signal the stock and False if there is no signal signal
    '''
    # These variables will be set to 'buy' if the technical indicators suggest to signal
    RSI = False
    pivot = False
    kelter = False
    macd = False
    signals_that_are_buy = []
    
    if RSI is not None:
        RSI = based_on_RSI(RSI)
        if RSI == 'buy':
            signals_that_are_buy.append("RSI")

    if pivot_support_1 is not None:
        pivot = based_on_pivot_points(price, pivot_support_1)
        if pivot == 'buy':
            signals_that_are_buy.append("Support1")

    if lower_keltner_channel is not None:
        kelter = based_on_keltner_channel(price, lower_keltner_channel)
        if kelter == 'buy':
            signals_that_are_buy.append("Keltner")

    if macd_line is not None and macd_signal is not None:
        macd = based_on_macd(macd_line, macd_signal)
        if macd == 'buy':
            signals_that_are_buy.append("MACD")

    if RSI == 'buy' and kelter == 'buy' and macd == 'buy' and pivot == 'buy':
        return (['buy', signals_that_are_buy])
    else:
        return (["No Signal", "None"])