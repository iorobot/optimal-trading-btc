import configargparse
from backfill.candles import Candles
from backfill.trades import Trades


arg_parser = configargparse.get_argument_parser()
options = arg_parser.parse_known_args()[0]

# add manually some options:
options.pairs = 'BTC_ETH'
options.days = 5
options.backfilltrades = True

print(options)
# Trades vs Canldes -> don't know the difference
if options.backfilltrades:
    backfill_client = Trades()
    backfill_client.run()
else:
    backfill_client = Candles()
    backfill_client.run()

# print mongodb collection
print(backfill_client.db_ticker)

# print first 10 canldes of mongodb
cursor = backfill_client.db_ticker.find({})
for document in cursor[:10]:
    print(document, '\n')



#class pippo:
#
#    pluto=5
#
#    def __init__(self):
#
#        return
#
#    def somma(self):
#
#        return pluto +5
#
#    def somma2(self):
#
#        return self.pluto + 5
#
#    @abstractmethod
#    def initialize_db():
#        return


