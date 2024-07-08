import sys
import pytz
sys.path.append('../')
import pandas as pd
from strategy.strategy import Strategy
import pandas_ta as ta
class KDJ_GAP(Strategy):
    def __init__(self):
        self.strategy_name = "KDJ_GAP"
        self.resolution = "daily" #realtime or daily
        self.timezone = pytz.timezone('America/New_York')
        #self.timezone = pytz.timezone('Asia/Hong_Kong')


    def check_trade_logic(self, profile):
        ticker = profile['ticker']
        df = pd.read_csv(f'data/{ticker}.csv')
        df2 = ta.kdj(high=df['High'], low = df['Low'], close=df['Close'])
        df = pd.concat([df,df2], axis=1)
        df=df.rename(columns={'K_9_3':'K',"D_9_3":"D","J_9_3":"J"})

        JK_len = profile[ticker]['parameters']['JK_LEN']
        JK_pos = profile[ticker]['parameters']['JK_Pos']
        z_score = profile[ticker]['parameters']['z-score']
        
        df['J-K'] = df['J'] - df['K']
        df['J-K_avg'] = df['J-K'].rolling(JK_len).mean()
        df['J-K_std'] = df['J-K'].rolling(JK_len).std()
        df['J-K_zscore'] = (df['J-K'] - df['J-K_avg']) / df['J-K_std']

        JK_zscore = df['J-K_zscore'].iloc[-1]
        JK_zscore_last_value = df['J-K_zscore'].iloc[-2]
        print(JK_zscore, JK_zscore_last_value, z_score, JK_pos)
        if JK_pos == True:
            trade_logic = (JK_zscore >= z_score) & (JK_zscore_last_value<z_score)
        else:
            z_score = z_score*-1
            trade_logic = (JK_zscore <= z_score) & (JK_zscore_last_value>z_score)

        return trade_logic

    
if __name__=="__main__":
    import sys
    sys.path.append('../')
    import os
    from app.models.ticker import Strategy
    strategy_name = os.getcwd().split('/')[-1]
    profiles = Strategy.objects(strategy=strategy_name).all()
    profiles = [profile.to_dict() for profile in profiles]

    my_kdj = KDJ_GAP()
    for profile in profiles:
        trade_logic = my_kdj.check_trade_logic(profile)
        print(profile.keys(), trade_logic)