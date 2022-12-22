# Investing
Code to help with stock investments (mainly which stocks are at a good time to sell a put or sell a call). BUY=stock will go up. Sell=stock will go down. We plan on adding in more technical indicators, but for right now ours works pretty well.


## Who is this for?
This tool and strategy is for investors looking to have above average returns while minimizing the risk that comes with investing in individual stocks. Using this strategy you will:
* Spend several weeks learning about basic options and investment principles
* Spend 30 minutes per week implimenting these strategies
* Ideally get 20-35% anual return on investment. This is not a garantee or financial advise, but an average of what we've seen. 
* Have 10,000 USD or more for investing in stable stocks

## Mailing list for options investors
This repository can be difficult to setup and costly to run nightly. Some users may not be able to run these tools because of a lack of internet speed. Instead, 
you can join our mailing list. By joining this mailing list you will receive:
* An investment cheatsheet for options investors
* An investment plan leveraging this tool
* Links and cheatsheets for trading the this options strategy
* One daily email(monday through friday before the market opens)
    * List of stable and reliable stocks
    * List of buy and sell signals as they occur. See "sell-signals.csv" for an example of what you might see.
    * Stocks that are added or removed from our stock list


We can add you to our mailing list for $30/month and you can cancel this at any time. There are no refunds. Email simonowens157@gmail.com to begin the signup and subscription process. 
## runtime overview
This script cannot easily be run. It takes roughly 12 hours(on an old server with 800mbs internet while runing in a docker container) to complete with fast internet because it searches through every stock in the NASDAQ and NYSE. You could run tasks in paralell but then you would be spamming Yahoo's public API. You could run this on AWS but it would cost more than joining the mailing list. It is best to run overnight slowly on a server as a scheduled task. The NASDAQ only has roughly 25% of the symbols we use as good stocks, but yet has 8000 of the 11000 total symbols we search through. NYSE has much more robust stocks in that exchange per our filters. 
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


If you want to see another technical indicator, open a request and site which books and professionals use this strategy with some examples. Once we see the value in this strategy we could work on implementing it.
## adding symbols
If you would like to add or remove any stocks from the list, you can:
* Open the "main.py" file
* Add or delete symbols from the varaibles "NASDAQ_symbols" and "NYSE_symbols"
* When adding symbols, it is important to add them to correct exchange

## scheduled tasks
* Purpose: this gets the latest changes from this repo, installs dependencies, and then runs the script every midnight when the markets will be open the next day. Results should be ready before 8am eastern time monday->Friday.
* utility: crontab
* 0 20 * * 0-4      = At 8pm EST on every day-of-week from Sunday through Thursday.
* path on simon's server: /media/apps/investing/update-and-run.sh
* internet speed: 800~mbs
* exact crontab line:
```
0 20 * * 0-4 /media/apps/investing/update-and-run.sh
```