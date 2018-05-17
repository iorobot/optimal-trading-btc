import configargparse
from core.engine import Engine # REMIND to change directory

# read and initialize some options
arg_parser = configargparse.get_argument_parser()
arg_parser.add('-c', '--config', is_config_file=True, help='config file path', default='mosquito.ini')
arg_parser.add('--backtest', help='Simulate your strategy on history ticker data', action='store_true')
arg_parser.add("--paper", help="Simulate your strategy on real ticker", action='store_true')
arg_parser.add("--live", help="REAL trading mode", action='store_true')
arg_parser.add('-v', '--verbosity', help='Verbosity', action='store_true')
arg_parser.add('--strategy', help='Strategy')
arg_parser.add('--fixed_trade_amount', help='Fixed trade amount')
args = arg_parser.parse_known_args()[0]

# add manually trade mode
args.backtest = True
# args.live = True
# args.paper = True


# usage
# print(arg_parser.format_help())

# print current options
print(args)

# check whether trade mode is provided, otherwise exit
if not args.backtest and not args.live and not args.paper:
    print("Missing trade mode argument (backtest, paper or live). See --help for more details.")
    exit(0)
else:
    # initialize and run Engine
    engine = Engine(trade_mode_input = 'backtest', plot_input = True, strategy = 'bumblebee')
    engine.run() # problems with exit


# data downloaded: pandas dataframe
data = engine.history
print(data.columns)
print(data.shape)
print(data.describe())
# dates = data.date


