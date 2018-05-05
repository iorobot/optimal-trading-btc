import time
import sys, getopt
import datetime
from poloniex import poloniex # REMEMBER TO CHANGE WORKING DIRECTORY


# initializing variables
period = 10
pair = "BTC_XMR"
prices = []
currentMovingAverage = 0;
lengthOfMA = 0
startTime = False
endTime = False
historicalData = False
tradePlaced = False
typeOfTrade = False
dataDate = ""
orderNumber = ""

# emulate opts & args from command line options: instead of changing the full code i adopt this approach
opts = [['-p','300'], 
        ['-s','1491048000'], 
        ['-e', '1491091200']
       ]

for opt, arg in opts:
    if opt == '-h':
        print 'trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>'
        sys.exit()
    elif opt in ("-p", "--period"):
        # period in seconds
        if (int(arg) in [300,900,1800,7200,14400,86400]):
            period = arg
        else:
            print 'Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments'
            sys.exit(2)
    elif opt in ("-c", "--currency"):
        # currency specification
        pair = arg
    elif opt in ("-n", "--points"):
        # moving average
        lengthOfMA = int(arg)
    elif opt in ("-s"):
        # start of time series for backtesting
        startTime = arg
    elif opt in ("-e"):
        # end of time series for backtesting
        endTime = arg

# connect to poloniex
conn = poloniex('key goes here','key goes here')

#if startTime is provided then download timeseries for backtesting as list of dicts
if (startTime):
    historicalData = conn.api_query("returnChartData",{"currencyPair":pair,"start":startTime,"end":endTime,"period":period})


while True:
    # if backtesting then pop holdest price 
    if (startTime and historicalData):
        nextDataPoint = historicalData.pop(0)
        lastPairPrice = nextDataPoint['weightedAverage']
        dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint['date'])).strftime('%Y-%m-%d %H:%M:%S')
    elif(startTime and not historicalData):
        # finished to read historical data
        # IMPORTANT: use break when debugging and exit() when launching from terminal
        # exit()
        break
    else:
        # if not backtesting
        currentValues = conn.api_query("returnTicker")
        lastPairPrice = currentValues[pair]["last"]
        dataDate = datetime.datetime.now()

    if (len(prices) > 0):
        # compute moving average
        currentMovingAverage = sum(prices) / float(len(prices))
        previousPrice = prices[-1]
        # trading strategy
        if (not tradePlaced):
            if ( (lastPairPrice > currentMovingAverage) and (lastPairPrice < previousPrice) ):
                print "SELL ORDER"
                #orderNumber = conn.sell(pair,lastPairPrice,.01)
                tradePlaced = True
                typeOfTrade = "short"
            elif ( (lastPairPrice < currentMovingAverage) and (lastPairPrice > previousPrice) ):
                print "BUY ORDER"
                #orderNumber = conn.buy(pair,lastPairPrice,.01)
                tradePlaced = True
                typeOfTrade = "long"
        elif (typeOfTrade == "short"):
            if ( lastPairPrice < currentMovingAverage ):
                print "EXIT TRADE"
                #conn.cancel(pair,orderNumber)
                tradePlaced = False
                typeOfTrade = False
        elif (typeOfTrade == "long"):
            if ( lastPairPrice > currentMovingAverage ):
                print "EXIT TRADE"
                #conn.cancel(pair,orderNumber)
                tradePlaced = False
                typeOfTrade = False
    else:
        previousPrice = 0

    print "%s Period: %ss %s: %s Moving Average: %s" % (dataDate,period,pair,lastPairPrice,currentMovingAverage)

    prices.append(float(lastPairPrice))
    prices = prices[-lengthOfMA:]
    if (not startTime):
        time.sleep(int(period))