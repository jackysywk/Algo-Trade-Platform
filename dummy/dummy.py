import sys

sys.path.append('../')
from strategy.strategy import Strategy

class Dummy(Strategy):
    def __init__(self):
        self.strategy_name = "dummy"
        self.resolution = "daily" #realtime or daily

    def check_trade_logic(self, profile):
        print(profile)
        return True