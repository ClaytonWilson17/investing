# Determine if you should signal a stock based on our own custom settings


def based_on_pivot_points(current_price, support_price_1, resistance_price_1):
    signal = None
    if float(current_price) <= float(support_price_1):
        signal = 'buy'
    elif float(current_price) >= float(resistance_price_1):
        signal = 'sell'
    else:
        signal = 'None'
        
    return (signal)




def determine_signals(price, pivot_resistance_1, pivot_support_1):

    '''
    All values except price are set to None by default, it will test whatever values you input to see if there is a signal on one of the indicators

    Returns 'buy' if you should signal the stock and False if there is no signal signal
    '''
    
    pivot = based_on_pivot_points(price, pivot_support_1, pivot_resistance_1)

    if pivot == 'buy':
        return (['buy', 'Support and Resistance'])
    elif pivot =='sell':
        return (['sell', 'Support and Resistance'])
    else:
        return (["No Signal", "None"])