# Test the custom_signal script
exec("""\nimport sys,os\nexec(\"\"\"\\ndef get_git_root(path=os.getcwd(),display=False):\\n    \\n    '''\\n    Get Git Root Directory. Only recursively goes up 10 directories.\\n    RETURNS: None or absolute path to git root directory\\n    '''\\n    count = 0\\n    prefix = ""\\n    while count < 10:\\n        if os.path.exists(prefix+'.git'):\\n            return os.path.abspath(prefix)\\n        else:\\n            prefix +="../"\\n            count+=1\\n    print("No git top level directory")\\n    return None\\n\"\"\")\ngitroot=get_git_root()\nsys.path.append(os.path.abspath(gitroot))\n""") # one liner statement that adds the root of this repo to python for inports
from helper_functions import custom_signal, general
from importlib import reload
reload(custom_signal)
import unittest
import os
from datetime import date, datetime, timedelta

## test all signals
class TestAllSignals(unittest.TestCase):
    def test_markus_buy_signals(self):
        data = []
        my_dict = {
            'Symbol': 'MCHP', 
            'Price': 84.88, 
            'RSI': 63.58571399, 
            'Pivot middle': 74.87333333, 
            'Pivot support 1': 71.15166667, 
            'Pivot support 2': 64.68333333, 
            'Pivot resistance 1': 81.34166667, 
            'Pivot resistance 2': 85.06333333, 
            'MACD_line': 2.97553562, 
            'MACD_signal': 2.72815476, 
            'Stochastic': 73.01666015, 
            'Keltner lower': 75.76683334, 
            'Keltner upper': 86.10966781
            }

        data.append(my_dict)
        path = custom_signal.determine_signals(data)
        
        self.assertTrue(path != 'none')


if __name__ == '__main__':
    unittest.main()