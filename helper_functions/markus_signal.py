# Determine if you should signal a stock (sell a put) based on technical indicators from Markus

def based_on_RSI(RSI, past_RSI):
    signal = None
    if float(RSI) < float(50):
        if float(RSI) < float(past_RSI):   
            signal = 'buy'
    return (signal)


def based_on_stochastic(stochastic, past_stochastic):
    signal = None
    if float(stochastic) < float(50):
        if float(stochastic) < float(past_stochastic):
            signal = 'buy'
    return (signal)


def based_on_macd(MACD_line):
    '''
    If the MACD line is below 0
    '''
    
    MACD_line = float(MACD_line)
    signal = None

    if float(MACD_line) < float(0):
        signal = 'buy'

    return (signal)


def determine_signals(RSI=None, past_RSI=None, stochastic=None, past_stochastic=None, macd_line=None):

    '''
    All values except price are set to None by default, it will test whatever values you input to see if there is a signal signal on one of the indicators

    Returns ['buy']
    '''
    # These variables will be set to 'buy' if the technical indicators suggest to signal
    RSI = False
    macd = False
    signals_that_are_buy = []
    
    if RSI is not None:
        RSI = based_on_RSI(RSI, past_RSI=past_RSI)
        if RSI == 'buy':
            signals_that_are_buy.append("RSI")

    if stochastic is not None:
        stoch = based_on_stochastic(stochastic=stochastic, past_stochastic=past_stochastic)
        if stoch == 'buy':
            signals_that_are_buy.append("stochastic")

    if macd_line is not None:
        macd = based_on_macd(macd_line)
        if macd == 'buy':
            signals_that_are_buy.append("MACD")

    if RSI == 'buy' and macd == 'buy' and stoch == 'buy':
        return (['buy', 'Markus'])
    else:
        return (["No Signal", "None"])