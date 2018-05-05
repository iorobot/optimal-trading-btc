#import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy

# Select chart on which we want to backtest the strategy
chart = BotChart("poloniex","BTC_XMR",300)

# print first value of the timeseries
print chart.getPoints()[0]


# define Bot Strategy
strategy = BotStrategy()

# Apply strategy
for candlestick in chart.getPoints():
    strategy.tick(candlestick)
