# retrieves all of the technical indicators needed to determine buy and sell signals
exec("""\nimport sys,os\nexec(\"\"\"\\ndef get_git_root(path=os.getcwd(),display=False):\\n    \\n    '''\\n    Get Git Root Directory. Only recursively goes up 10 directories.\\n    RETURNS: None or absolute path to git root directory\\n    '''\\n    count = 0\\n    prefix = ""\\n    while count < 10:\\n        if os.path.exists(prefix+'.git'):\\n            return os.path.abspath(prefix)\\n        else:\\n            prefix +="../"\\n            count+=1\\n    print("No git top level directory")\\n    return None\\n\"\"\")\ngitroot=get_git_root()\nsys.path.append(os.path.abspath(gitroot))\n""") # one liner statement that adds the root of this repo to python for inports
from helper_functions import get_fundamental_indicators, general
from importlib import reload
reload(get_fundamental_indicators)
import unittest
import os
from datetime import date, datetime, timedelta

## is_composite_stock
class TestCompositeStock(unittest.TestCase):
    def test_is_composite_stock_true(self):
        stock_info = {'symbol': '^IXIC'}
        self.assertTrue(get_fundamental_indicators.is_composite_stock(stock_info, "^IXIC"))

    def test_is_goog_false(self):
        stock_info = {'symbol': 'GOOGL'}
        self.assertFalse(get_fundamental_indicators.is_composite_stock(stock_info, 'GOOGL'))
        
    def test_is_short_composite_true(self):
        stock_info = {'symbol': 'DJI'}
        self.assertTrue(get_fundamental_indicators.is_composite_stock(stock_info, 'DJI'))

    def test_is_blank_stock_false(self):
        stock_info = {'symbol': ''}
        self.assertFalse(get_fundamental_indicators.is_composite_stock(stock_info, ""))

    def test_is_empty_false(self):
            stock_info = {}
            self.assertFalse(get_fundamental_indicators.is_composite_stock(stock_info, None))

## get_all_symbols
class TestgetAllSymbols(unittest.TestCase):
    def test_retrieved_symbols_are_greater_than_10k(self):
        values = get_fundamental_indicators.get_all_symbols()
        self.assertGreater(len(values), 10000) # there are always atleast 10k symbols in the indexes

## get_all_symbol_object
class TestgetAllSymbolObject(unittest.TestCase):
    def test_retrieved_symbol_objects_added_the_indexes(self):
        values = len(get_fundamental_indicators.get_all_symbols())
        values_plus_2 = len(get_fundamental_indicators.get_all_symbol_object())#two indexes, ixic and nya are being added here
        self.assertEqual(values+2, values_plus_2)

        blacklist = [{'symbol': "GOOG", 'exchange': "NASDAQ"}, {'symbol': "DUK", 'exchange': "NYSE"}]
        values_minus_2 = len(get_fundamental_indicators.get_all_symbol_object(blacklist=blacklist))
        self.assertEqual(values, values_minus_2)

## get_symbol_object
class TestgetSymbolObject(unittest.TestCase):
    def test_retrieved_symbol(self):
        value = get_fundamental_indicators.get_symbol_object("GOOG", "NASDAQ")
        test = value['symbol']
        self.assertEqual(test, 'GOOG') # there are always atleast 10k symbols in the indexes

## get_good_stock_data
stock_keys = ['shortName', 'industry', 'symbol', 'exchange', 'currentPrice', 'marketCap', 'heldPercentInstitutions', 'dividendYield', 'exDividendDate', 'forwardEps', 'trailingEps', 'forwardPE', 'trailingPE', 'priceToBook', 'profitMargins', 'totalRevenue', 'grossProfits', 'returnOnAssets', 'returnOnEquity', 'debtToEquity', 'sharesOutstanding', 'floatShares', 'nextEarningsDate', '4Quarters_increasing_revenue', '4Quarters_increasing_profit', '4years_increasing_revenue', '4years_increasing_profit', 'pct_chg_5y', 'pct_chg_1y', 'pct_chg_6mo', 'pct_chg_3mo', 'pct_chg_1mo', 'pct_chg_1wk', 'fundamentals_url', 'daily_chart', '5mo_chart']
class Testget_good_stock_data(unittest.TestCase):
    def test_retrieved_good_stock(self):
        self.maxDiff = None
        stock = get_fundamental_indicators.get_symbol_object("ADI", "NASDAQ")
        value = get_fundamental_indicators.get_good_stock_data(stock, get_any_stock=True)
        self.assertEqual(list(value.keys()), stock_keys)

## write_symbol_to_csv
## correct keys for the stock object
csv_cleaned_keys = ['shortName', 'industry', 'symbol', 'exchange', 'currentPrice', 'heldPercentInstitutions', 'dividendYield', 'exDividendDate', 'forwardPE', 'trailingPE', 'priceToBook', 'nextEarningsDate', '4Quarters_increasing_revenue', '4Quarters_increasing_profit', '4years_increasing_revenue', '4years_increasing_profit', 'pct_chg_5y', 'pct_chg_1y', 'pct_chg_6mo', 'pct_chg_3mo', 'pct_chg_1mo', 'pct_chg_1wk', 'fundamentals_url', 'daily_chart', '5mo_chart']
class Testget_write_symbol_to_csv(unittest.TestCase):
    ### good stock - ADI
    def test_csv_retrieved_good_stock(self):
        value = get_fundamental_indicators.write_symbol_to_csv("ADI", "NASDAQ", cache=False)
        self.assertEqual(list(value.keys()), csv_cleaned_keys)
        ### CSV exists
        file_path = general.resultsPath("ADI_stock_data.csv")
        assert os.path.exists(file_path)
        ### cache exists
        value = get_fundamental_indicators.write_symbol_to_csv("ADI", "NASDAQ", cache=True)
        self.assertEqual(list(value.keys()), csv_cleaned_keys)
        file_path = general.dataPath("ADI_stock_data"+str(date.today())+".pkl")
        assert os.path.exists(file_path)
        ### correct keys
        self.assertEqual(list(value.keys()), csv_cleaned_keys)
        
    ### bad stock - google
    def test_csv_didnt_retrieve_bad_stock(self):
        value = get_fundamental_indicators.write_symbol_to_csv("GOOG", "NASDAQ", cache=False)
        self.assertEqual(value, None)
    
    ### get_any_stock - bad stock
    def test_csv_retrieve_bad_stock_via_any_stock_option(self):
        value = get_fundamental_indicators.write_symbol_to_csv("GOOG", "NASDAQ", cache=False, get_any_stock=True)
        self.assertEqual(list(value.keys()), csv_cleaned_keys)

    ### get_any_stock - good stock
    def test_csv_retrieve_good_stock_via_any_stock_option(self):
        value = get_fundamental_indicators.write_symbol_to_csv("ADI", "NASDAQ", cache=True, get_any_stock=True)
        self.assertEqual(list(value.keys()), csv_cleaned_keys)
        value = get_fundamental_indicators.write_symbol_to_csv("ADI", "NASDAQ", cache=False, get_any_stock=True)
        self.assertEqual(list(value.keys()), csv_cleaned_keys)

    ### get_any_stock - index
    def test_csv_retrieve_index_via_any_stock_option(self):
        value = get_fundamental_indicators.write_symbol_to_csv("^IXIC", "NASDAQ", cache=False, get_any_stock=True)
        self.assertEqual(list(value.keys()), csv_cleaned_keys)
        value = get_fundamental_indicators.write_symbol_to_csv("^NYA", "NYSE", cache=False, get_any_stock=True)
        self.assertEqual(list(value.keys()), csv_cleaned_keys)

## write_symbols_to_csv - 7 added(2 index, 5 stocks, 1 stock on blacklist), 2 blacklist stocks, no_all
class Testget_write_symbols_to_csv(unittest.TestCase):
    ### good stocks
    def test_all_csv_retrieved_good_stocks(self):
        added=[{'symbol': "GOOG", 'exchange': "NASDAQ"},{'symbol': "ADI", 'exchange': "NASDAQ"},{'symbol': "CNI", 'exchange': "NYSE"},{'symbol': "CAT", 'exchange': "NASDAQ"},{'symbol': "V", 'exchange': "NYSE"},{'symbol': "^IXIC", 'exchange': "NASDAQ"},{'symbol': "^NYA", 'exchange': "NYSE"}]
        blacklist=[{'symbol': "GOOG", 'exchange': "NASDAQ"}, {'symbol': "DUK", 'exchange': "NYSE"}]
        value = get_fundamental_indicators.write_symbols_to_csv(added_tickers=added, blacklisted_tickers=blacklist,do_all_tickers=False)
        self.assertEqual(len(value), 6) #7added-1blacklist=6


## get_delta
### no data
### symbol added
### symbol removed


if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestSuite()
    #suite.addTest(Testget_good_stock_data("test_retrieved_good_stock"))
    #unittest.TextTestRunner().run(suite)