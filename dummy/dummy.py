import sys
import pytz
sys.path.append('../')
from strategy.strategy import Strategy

class Dummy(Strategy):
    def __init__(self):
        self.strategy_name = "dummy"
        self.resolution = "daily" #realtime or daily
        self.timezone = pytz.timezone('America/New_York')
        #self.timezone = pytz.timezone('Asia/Hong_Kong')

    def check_trade_logic(self, profile):
        print(profile)
        return True