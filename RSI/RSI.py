import sys
import pytz
sys.path.append('../')
import pandas as pd
from strategy.strategy import Strategy
import pandas_ta as ta
class RSI(Strategy):
    def __init__(self):
        self.strategy_name = "RSI"
        self.resolution = "daily" #realtime or daily
        self.timezone = pytz.timezone('America/New_York')
        #self.timezone = pytz.timezone('Asia/Hong_Kong')


    def check_trade_logic(self, profile):
        ticker = profile['ticker']
        #ticker = list(profile.keys())[0]
        df = pd.read_csv(f'data/{ticker}.csv')
        df['rsi'] = ta.rsi(df['Close'],length=14)
        rsi_value = df['rsi'].iloc[-1]
        rsi_last_value = df['rsi'].iloc[-2]
        rsi_type = profile[ticker]['parameters']['RSI']
        rsi_thresold = profile[ticker]['parameters']['RSI_Thresold']
        if rsi_type == 'Cross Over':
            trade_logic = (rsi_value > rsi_thresold) & (rsi_last_value <= rsi_thresold)
        elif rsi_type == 'Cross Under':
            trade_logic = (rsi_value < rsi_thresold) & (rsi_last_value >= rsi_thresold)
        else:
            trade_logic=  False
        return trade_logic

    
if __name__=="__main__":
    import sys
    sys.path.append('../')
    import os
    from app.models.ticker import Strategy
    strategy_name = os.getcwd().split('/')[-1]
    profiles = Strategy.objects(strategy=strategy_name).all()
    profiles = [profile.to_dict() for profile in profiles]
    my_rsi = RSI()
    for profile in profiles:
        trade_logic = my_rsi.check_trade_logic(profile)
        print(profile.keys(), trade_logic)
    sys.exit()