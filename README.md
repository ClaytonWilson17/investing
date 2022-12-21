# Investing
Code to help with stock investments (mainly which stocks are at a good time to sell a put or sell a call). BUY=stock will go up. Sell=stock will go down. We plan on adding in more technical indicators, but for right now ours works pretty well.

## Instructions
This script cannot easily be run. It takes roughly 12 hours(on an old server with 800mbs internet while runing in a docker container) to complete with fast internet because it searches through every stock in the NASDAQ and NYSE. You could run tasks in paralell but then you would be spamming Yahoo's public API. It is best to run overnight slowly on a server as a scheduled task. The NASDAQ only has roughly 25% of the symbols we use as good stocks, but yet has 8000 of the 11000 total symbols we search through. NYSE has much more robust stocks in that exchange per our filters. We can add you to our mailing list for $30 bucks a month and you can canel this at any time. Email investingbot2@gmail.com to begin the signup subscription process. You will receive:
* One daily email(monday through friday before the market opens)
* List of good stocks
* List of buy and sell signals as they occur
* Stocks that are added or removed from our stock list
See "sell-signals.csv" for an example of what you might see.
## Environment variables
Please add these environment variables to a .env file with their values
```
symbols_api_key=
GMAIL=
simon_email=
clayton_email=
```
You will have to alter the code to send to different email's if those environment names bother you.

## Fundamental indicators
We choose stocks based on guidance from markus heitkoetter. We don't invest in small or medium cap stocks. And we generally only invest in reliable stocks (generally not the popular tech stocks). We then trade options on those reliable stocks. Could we make more money? sure. But our target is 20-30% yearly return while minimizing risk of being stuck in a position for more than 1 year. Mistakes will happen but that is our plan.
## Technical indicators
1. Our script will finish early morning before the stock market opens. Say 5-10-2022
2. Our script will look at the yesterday's technical indicators to determine if indicators are going up, or down. Say 5-9-2022
3. As a result, 5-9-2022 technical data is BEFORE the market opened. 5-10-2022 is AFTER the market closed. Both really occuring on 5-9-2022. 
## adding symbols
If you would like to add or remove any stocks from the list, you can:
* Open the "main.py" file
* Add or delete symbols from the varaibles "NASDAQ_symbols" and "NYSE_symbols"
* When adding symbols, it is important to add them to correct exchange

## scheduled tasks
* Purpose: this gets the latest changes from this repo, installs dependencies, and then runs the script every midnight when the markets will be open the next day. Results should be ready before 8am eastern time monday->Friday.
* utility: crontab
* 0 16 * * 0-4      = At 6pm EST on every day-of-week from Sunday through Thursday.
* path on simon's server: /media/apps/investing/update-and-run.sh
* internet speed: 800~mbs
* exact crontab line:
```
0 16 * * 0-4 /media/apps/investing/update-and-run.sh
```