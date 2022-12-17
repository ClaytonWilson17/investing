# Determine if you should signal a stock (sell a put) based on technical indicators from Markus

def based_on_RSI(RSI, past_RSI):
    signal = None
    if float(RSI) > float(50):
        if float(RSI) > float(past_RSI):   
            signal = 'buy'
    
    if float(RSI) < float(50):
        if float(RSI) < float(past_RSI):   
            signal = 'sell'
    return (signal)


def based_on_stochastic(stochastic, past_stochastic):
    signal = None
    if float(stochastic) > float(50):
        if float(stochastic) > float(past_stochastic):
            signal = 'buy'

    if float(stochastic) < float(50):
        if float(stochastic) < float(past_stochastic):
            signal = 'sell'
    return (signal)


def based_on_macd(MACD_line, signal_line):
    '''
    If the MACD line is greater than the signal line (market in uptrend)
    '''
    
    MACD_line = float(MACD_line)
    signal_line = float(signal_line)
    signal = None
    if MACD_line > signal_line:
        signal = 'buy'
    
    if MACD_line < signal_line:
        signal = 'sell'

    return (signal)


def determine_buy_signals(RSI=None, past_RSI=None, stochastic=None, past_stochastic=None, macd_line=None, macd_signal=None):

    '''
    All values except price are set to None by default, it will test whatever values you input to see if there is a signal signal on one of the indicators

    Returns ['buy', [signals]]
    '''
    # These variables will be set to 'buy' if the technical indicators suggest to signal
    
    
    signals_that_are_buy = []
    
    if RSI is not None:
        RSI_signal = based_on_RSI(RSI, past_RSI=past_RSI)
        if RSI_signal == 'buy':
            signals_that_are_buy.append("RSI")

    if stochastic is not None:
        stoch = based_on_stochastic(stochastic=stochastic, past_stochastic=past_stochastic)
        if stoch == 'buy':
            signals_that_are_buy.append("stochastic")

    if macd_line is not None and macd_signal is not None:
        macd = based_on_macd(macd_line, macd_signal)
        if macd == 'buy':
            signals_that_are_buy.append("MACD")
    
    if (RSI_signal == 'buy' and macd == 'buy' and stoch == 'buy'):
        
        return (['buy', signals_that_are_buy])
    else:
        return (["No Signal", "None"])


def determine_sell_signals(RSI=None, past_RSI=None, stochastic=None, past_stochastic=None, macd_line=None, macd_signal=None):
    
    '''
    All values except price are set to None by default, it will test whatever values you input to see if there is a signal signal on one of the indicators

    Returns ['sell', [signals]]
    '''
    # These variables will be set to 'buy' if the technical indicators suggest to signal
    
    macd = ''
    stoch = ''
    signals_that_are_sell = []
    
    if RSI is not None:
        RSI = based_on_RSI(RSI, past_RSI=past_RSI)
        if RSI == 'sell':
            signals_that_are_sell.append("RSI")

    if stochastic is not None:
        stoch = based_on_stochastic(stochastic=stochastic, past_stochastic=past_stochastic)
        if stoch == 'sell':
            signals_that_are_sell.append("stochastic")

    if macd_line is not None and macd_signal is not None:
        macd = based_on_macd(macd_line, macd_signal)
        if macd == 'sell':
            signals_that_are_sell.append("MACD")

    if (RSI == 'sell' and macd == 'sell' and stoch == 'sell'):
        return (['sell', signals_that_are_sell])
    else:
        return (["No Signal", "None"])