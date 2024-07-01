from mongoengine import Document, StringField, BooleanField,IntField, DateTimeField, DynamicField, FloatField
from datetime import datetime

class Ticker(Document):
    meta = {'collection': 'tickers'}
    ticker = StringField(required=True)
    market = StringField(required=True)
    secType = StringField(required=True)
    primaryExchange=StringField()

    def to_dict(self):
        return {"id":str(self.id),
                "ticker": self.ticker,
                "market": self.market,
                "secType": self.secType,
                "primaryExchange":self.primaryExchange
                }

class Strategy_list(Document):
    meta={'collection':'strategy_list'}
    strategy = StringField(required=True)

    def to_dict(self):
        return {"id":str(self.id),
                "strategy": self.strategy,
                }

class Strategy(Document):
    meta = {'collection':'strategy'}
    strategy = StringField(required=True)
    ticker = StringField(required=True)
    market = StringField(required=True)
    secType = StringField(required=True)
    parameters = DynamicField(required=True)
    active = BooleanField(required=True)
    state = StringField(required=True)
    quantity = IntField()
    open_price = FloatField()
    open_position_time = DateTimeField()
    orderId = IntField()
    '''
    State workflow
    1. Monitoring Signal
    2. Strategy Stopped
    3. Signal Detected
    4. Opening Order
    5. Open Position
    6. Selling Order
    '''
    update_time = DateTimeField(required=True)
    last_logic_time = DateTimeField(required=True)

    def __repr__(self):
        return f'<Strategy {self.strategy!r} - {self.ticker!r} - {self.market!r}>'

    def to_dict(self):
        return {self.ticker:{
                "strategy": self.strategy,
                "ticker": self.ticker,
                'market':self.market,
                'secType':self.secType,
                "parameters": self.parameters,
                "active":self.active,
                "state":self.state,
                "quantity":self.quantity,
                "orderId":self.orderId if self.orderId else None,
                "open_price":self.open_price,
                "open_position_time":self.open_position_time.isoformat() if self.open_position_time else None,
                "update_time":self.update_time.isoformat(),
                "last_logic_time":self.last_logic_time.isoformat()
                }}

    def get_open_position_time(self):
        return {"strategy":self.strategy,
                "ticker":self.ticker,
                "open_position_time":self.open_position_time.isoformat() if self.open_position_time else None}
    
    def get_open_price(self):
        return {"strategy":self.strategy,
                "ticker":self.ticker,
                "open_price":self.open_price}
    
    def get_open_qty(self):
        return {"strategy":self.strategy,
                "ticker":self.ticker,
                "quantity":self.quantity}
    def get_orderId(self):
        return {"strategy":self.strategy,
                "ticker":self.ticker,
                "orderId":self.orderId if self.orderId else None}


from mongoengine import connect
if __name__ == "__main__":
    connect(db='mydatabase', 
        host='localhost', 
        port=27017,
        username = 'rootuser',
        password = 'rootpass')
    
    stock_profile = [
    {'ticker':"META",
    'parameters':{
        'PT':10,
        'SL':2.5,
        'HD':20,
        "JK_len":250,
        'JK_positive':False,
        'z-score':1.5,
        'trade_time':'morning'
    }
    },
    {'ticker':"MA",
        'parameters':{
            'PT':10,
            'SL':2.5,
            'HD':20,
            "JK_len":50,
            'JK_positive':False,
            'z-score':1,
            'trade_time':'afternoon'
        }
    },
    ]
    strategy = 'KDJ_gap'
    if Strategy_list.objects(strategy=strategy).first():
        print("Strategy already exist")
    else:
        new_strategy = Strategy_list(strategy=strategy)
        new_strategy.save()
        print(f"Create a new Strategy - {strategy}")

    for stock in stock_profile:
        print(stock)
        existing_ticker = Strategy.objects(ticker=stock['ticker']).first()
        if existing_ticker:
            existing_ticker.update(
            set__strategy = strategy,
            set__ticker = stock['ticker'],
            set__active = True,
            set__state = 'Monitoring Signal',
            set__update_time=datetime.now(),
            set__last_logic_time = datetime.now(),
            set__parameters = stock['parameters'],
            set__market = 'US',
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
                last_logic_time = datetime.now(),
                parameters = stock['parameters'],
                market = 'US',
                quantity = 0
            )
            new_strategy.save()
            print("Inserted a new strategy for ticker:", stock['ticker'])
