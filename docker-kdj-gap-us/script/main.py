from kafka import KafkaConsumer
import requests
from datetime import datetime
import json
class Ticker:
    def __init__(self, profile):
        self.ticker = profile['ticker']
        self.state = profile['state'] 
        self.qty = profile['quantity'] 
        self.parameters = profile['parameters'] 
        self.market = profile['market']
        if self.market == 'US':
            self.lot_size = 1
        self.order_id = None
        self.trade_logic = None
        self.trading_time = profile['parameters']['trade_time']
        self.last_logic_time = datetime.strptime(profile['last_logic_time'],"%Y-%m-%dT%H:%M:%S.%f")
        self.bid_ask_dict = {
            'bid' : None,
            'bid_timestamp' : datetime(2020,7,1,0,0),
            'ask': None,
            'ask_timestamp': datetime(2020,7,1,0,0),
            'last_price': None,
            'last_price_timestamp':datetime(2020,7,1,0,0)
        }

    def check_trade_logic(self):
        ### To be implemented
        return False
    def monitoring_signal(self):
        if datetime.now().date() > self.last_logic_time.date():
            trade_logic = self.check_trade_logic()
            if trade_logic:
                self.state = "Signal Detected"
                # API Change Mongo DB
                
    '''
    State workflow
    1. Monitoring Signal
    2. Strategy Stopped
    3. Signal Detected
    4. Opening Order
    5. Open Position
    6. Selling Order
    '''

strategy = 'KDJ_gap'
tickers = {}
if __name__ == "__main__": 
    # Getting Strategy Particular Dictionary from Flask API
    profiles = requests.get(f"http://localhost:8080/api/strategy/{strategy}").json()
    for ticker, profile in profiles.items():
        # Initialize a tickers dictionary storing ticker objects
        tickers[ticker] = Ticker(profile)

    # Starting Kafka Consumer
    while True:
        consumer = KafkaConsumer(
            bootstrap_servers = "localhost:9092",
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        )
        # profile.keys = list of ticker under this strategies
        consumer.subscribe(profiles.keys())
        for message in consumer:
            state = tickers[message.topic].state
            print(message.topic,state)



