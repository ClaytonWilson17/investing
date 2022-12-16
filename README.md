# Investing
Code to help with stock investments (mainly which stocks are at a good time to sell a put or sell a call)

## Instructions
* 

## Additional Info
If you would like to add or remove any stocks from the list, you can:
* Open the "main.py" file
* Add or delete symbols from the varaibles "NASDAQ_symbols" and "NYSE_symbols"
* When adding symbols, it is important to add them to correct exchange

## scheduled tasks
* Purpose: this gets the latest changes from this repo, installs dependencies, and then runs the script every midnight when the markets will be open the next day. Results should be ready before 8am eastern time monday->Friday.
* utility: crontab
* 0 0 * * 0-4      = At 00:00 on every day-of-week from Sunday through Thursday.
* path on simon's server: /media/config/investing/update-and-run.sh
* internet speed: 800~mbs
* exact crontab line:
```
0 0 * * 0-4 /media/config/investing/update-and-run.sh
```