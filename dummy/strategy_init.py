from mongoengine import connect
import sys
sys.path.append('../')
from app.models.ticker import Strategy, Strategy_list, Ticker
from datetime import datetime, timedelta
'''
This is a dummpy strategy.  
Trade Logic:
If yesterday stock price open > stock price close buy
PT =0.3
ST = 0.5
HD = 1

'''
if __name__ == "__main__":
    connect(db='mydatabase', 
        host='localhost', 
        port=27017,
        username = 'rootuser',
        password = 'rootpass')
    
    stock_profile = [
    {'ticker':"AAPL",
     'market':'US',
     'secType':'STK',
    'parameters':{
        'PT':0.1,
        'SL':0.1,
        'HD':1,
        'trade_time':'morning'
    }
    },
    {'ticker':"NVDA",
    'market':'US',
    'secType':'STK',
    'parameters':{
        'PT':0.1,
        'SL':0.1,
        'HD':1,
        'trade_time':'morning'
    }
    },
    ]
    strategy = 'dummy'
    if Strategy_list.objects(strategy=strategy).first():
        print("Strategy already exist")
    else:
        new_strategy = Strategy_list(strategy=strategy)
        new_strategy.save()
        print(f"Create a new Strategy - {strategy}")

    for stock in stock_profile:
        existing_ticker = Ticker.objects(ticker = stock['ticker']).first()
        if not existing_ticker:
            new_ticker = Ticker(
                ticker = stock['ticker'],
                market = stock['market'],
                secType = stock['secType']
            )
            new_ticker.save()

        existing_strategy = Strategy.objects(strategy = strategy,
                                             ticker=stock['ticker']).first()
        if existing_strategy:
            existing_strategy.update(
            set__strategy = strategy,
            set__ticker = stock['ticker'],
            set__active = True,
            set__state = 'Monitoring Signal',
            set__update_time=datetime.now(),
            set__last_logic_time = datetime.now()-timedelta(days=3),
            set__parameters = stock['parameters'],
            set__market = stock['market'],
            set__secType = stock['secType'],
            set__quantity = 0
            )
            print("Updated existing strategy for ticker:", stock['ticker'])
        else:
            new_strategy = Strategy(
                strategy = strategy,
                ticker = stock['ticker'],
                active = True,
                state = 'Monitoring Signal',
                update_time=datetime.now(),
                last_logic_time = datetime.now()-timedelta(days=3),
                parameters = stock['parameters'],
                market = stock['market'],
                secType = stock['secType'],
                quantity = 0
            )
            new_strategy.save()
            print("Inserted a new strategy for ticker:", stock['ticker'])
