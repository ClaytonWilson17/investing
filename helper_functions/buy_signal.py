# Determine if you should buy a stock (sell a put) based on technical indicators

def buy_based_on_RSI(RSI):
    buy = False
    if RSI < 31:    
        buy = True
    return (buy)


def buy_based_on_pivot_points(current_price, support_price_1):
    buy = False
    if current_price <= support_price_1:
        buy = True
    return (buy)


def buy_based_on_keltner_channel(current_price, bottom_channel):
    buy = False
    if current_price <= bottom_channel:
        buy = True
    return (buy)


def buy_based_on_macd(MACD_line, MACD_signal):
    '''
    If the MACD line and signal line cross while they are below the zero line, signal to buy the stock
    '''
    buy = False
    difference = abs(MACD_line - MACD_signal)

    # The value is set to .15 but may need to be changed, i am not sure if the values will ever actually hit 0 exactly
    if (difference < .15) and (MACD_line < 0): 
        buy = True

    return(buy)


def determine_buy_signals(price, RSI, pivot_support_1, lower_keltner_channel, macd_line, macd_signal, ):

    '''
    Returns a dictionary with keys that will be set to true if you should buy based on that indicator
    
    Dictionary Keys: buy_RSI, buy_pivot, buy_keltner, buy_macd
    '''
    # These variables will be set to true if the technical indicators suggest to buy
    buy_RSI = False
    buy_pivot = False
    buy_kelter = False
    buy_macd = False
    
    buy_RSI = buy_based_on_RSI(RSI)
    buy_pivot = buy_based_on_pivot_points(price, pivot_support_1)
    buy_kelter = buy_based_on_keltner_channel(price, lower_keltner_channel)
    buy_macd = buy_based_on_macd(macd_line, macd_signal)

    buy_signals = {
        "buy_RSI": buy_RSI,
        "buy_pivot": buy_pivot,
        "buy_keltner": buy_kelter,
        "buy_macd": buy_macd
    }
    
    return buy_signals