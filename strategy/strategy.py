from datetime import datetime, timedelta
import requests
from math import ceil

class Strategy:

    def __init__(self, ticker_list):
        self.ticker_list = ticker_list
        self.bid_ask_dict = {}
        self.profile = {}
        self.ticker_list = []

    def get_strategy_profile(self):
        form_data = {
            "strategy":self.strategy_name
        }
        strategy_dict = requests.post("http://localhost:8080/api/strategy", data = form_data).json()
        ticker_list = list(strategy_dict.keys())
        self.profile = strategy_dict
        self.ticker_list = ticker_list

    def update_ticker_state(self, ticker, state):
        form_data = {
            "strategy":self.strategy_name,
            "ticker":ticker,
            "state":state
        }
        res = requests.post("http://localhost:8080/api/update_strategy_state", data = form_data)
        print(res.text)


    def get_bid_ask_dict(self):
        bid_ask_dict={}
        for ticker in self.ticker_list:
            bid_ask_dict[ticker] = {}
            bid_ask_dict[ticker]['bid'] = None
            bid_ask_dict[ticker]['bid_timestamp'] = datetime(2020,7,1,0,0)
            bid_ask_dict[ticker]['ask'] = None
            bid_ask_dict[ticker]['ask_timestamp'] = datetime(2020,7,1,0,0)
            bid_ask_dict[ticker]['last_price'] = None
            bid_ask_dict[ticker]['last_price_timestamp'] = datetime(2020,7,1,0,0)
        return bid_ask_dict
    

def make_purchase_order(profile, qty, price):
    secType = profile['secType']
    symbol = profile['ticker']
    print(f"{symbol} make purchase order")
    form_data = {
        "secType":secType,
        "symbol":symbol,
        "action":"BUY",
        "qty" : qty,
        "price":price
    }
    res = requests.post("http://localhost:8080/api/place_order", data = form_data)
    return res.json()
    
    
def make_sell_order(profile, qty, price):
    
    secType = profile['secType']
    symbol = profile['ticker']
    print(f"{symbol} make sell order")
    form_data = {
        "secType":secType,
        "symbol":symbol,
        "action":"SELL",
        "qty" : qty,
        "price":price
    }
    res = requests.post("http://localhost:8080/api/place_order", data = form_data)
    return res.json()
    


def bid_ask_isvalid(bid_ask_dict, ticker):
    if (datetime.now() - bid_ask_dict[ticker]['bid_timestamp'] < timedelta(minutes=5)) and \
    (datetime.now() - bid_ask_dict[ticker]['ask_timestamp'] < timedelta(minutes=5)) and \
    (datetime.now() - bid_ask_dict[ticker]['last_price_timestamp'] < timedelta(minutes=5)):
        return True
    else:
        return False


def check_holding_days(strategy_obj):
    strategy = strategy_obj['strategy']
    ticker = strategy_obj['ticker']
    HD = strategy_obj['parameters']['HD']
    # get open position date
    form_data = {
        "strategy":strategy,
        "ticker": ticker
    }
    res = requests.post("http://localhost:8080/api/get_open_position_time", data = form_data)
    if (strategy == res['strategy']) and (ticker == res['ticker']):
        open_date = datetime.fromisoformat(res['open_position_time'].replace("Z","+00:00"))
    else:
        return False, "Data Error / API Error"
    diff = datetime.now() - open_date
    diff = diff.total_seconds() / 24 / 3600
    diff = ceil(diff)
    if diff >= HD:
        return True, "Holding Day Met"
    else:
        return False, "Holding Day Not Met"


 
def check_pt_sl(strategy_obj,last_price):
    strategy = strategy_obj['strategy']
    ticker = strategy_obj['ticker']
    PT = strategy_obj['parameters']['PT']
    SL = strategy_obj['parameters']['SL']
    # get open price using api
    form_data = {
        "strategy":strategy,
        "ticker":ticker
    }
    res = requests.post("http://localhost:8080/api/get_open_price", data = form_data).json()
    if (strategy == res['strategy']) and (ticker == res['ticker']):
        open_price = res['open_price']
    else:
        return False, "Data Error / API Error"
    print(f"{ticker}: open price:{open_price}, last price: {last_price}, PT: {open_price * (1+PT/100)}, SL:{open_price * (1-SL/100)}")
    if last_price >= open_price * (1+PT/100):
        print(f"{ticker}: Profit Target")
        return True, "Profit Target"
    elif last_price <= open_price * (1-SL/100):
        print(f"{ticker}: Stop Loss")
        return True, "Stop Loss"
    else:
        return False, "No Target Met"
def get_order_qty(strategy_obj):
    strategy = strategy_obj['strategy']
    ticker = strategy_obj['ticker']
    form_data = {
        "strategy":strategy,
        "ticker":ticker
    }
    res = requests.post("http://localhost:8080/api/get_open_qty", data=form_data).json()
    if (strategy == res['strategy']) and (ticker == res['ticker']):
        qty = res['quantity']
        return True, qty
    else:
        return False, "Data Error / API Error"



def update_orderId(strategy_obj, orderId):
    strategy = strategy_obj['strategy']
    ticker = strategy_obj['ticker']
    form_data = {
        'strategy':strategy,
        "ticker":ticker,
        "orderId":orderId
    }
    res = requests.post("http://localhost:8080/api/update_orderId", data=form_data)
    res = res.json()
    if res['RET'] != "OK":
       print("OrderID not updated")
    else:
        print(f"{ticker} Order ID updated") 

def get_orderId(strategy_obj):
    strategy = strategy_obj['strategy']
    ticker = strategy_obj['ticker']
    form_data = {
        'strategy':strategy,
        "ticker":ticker
    }
    res = requests.post("http://localhost:8080/api/get_orderId", data=form_data)
    res = res.json()
    if (strategy == res['strategy']) and (ticker == res['ticker']):
        orderId = res['orderId']
        return True, orderId
    else:
        return False, None
    
def check_execution(strategy_obj,orderId):
    strategy = strategy_obj['strategy']
    ticker = strategy_obj['ticker']
    res = requests.get("http://localhost:8080/api/fetch_orders")
    orders = res.json()
    for order in orders:
        if order['orderId'] == orderId:
            print(f"{ticker} Order {orderId} Not yet executed")
            return False, None
    
    res = requests.get("http://localhost:8080/api/fetch_execution")
    executions = res.json()

    for exe in executions:
        if exe['orderId'] == orderId:
            form_data = {
                'strategy':strategy,
                "ticker":ticker,
                "open_qty":exe['shares'],
                "open_price":exe['price']
            }
            res = requests.post("http://localhost:8080/api/update_order_execution", data=form_data).json()
            if res["RET"] != "OK":
                print("Update DB Error in execution order")
            print("Order executed")
            return True, exe['execId']
    print("Execution Not yet fetched")
    return False, None

def update_last_logic_time(strategy_obj):
    strategy = strategy_obj['strategy']
    ticker = strategy_obj['ticker']
    form_data = {
        'strategy':strategy,
        "ticker":ticker,
    }
    res = requests.post("http://localhost:8080/api/update_logic_time", data=form_data)
    res = res.json()
    if res['RET'] != "OK":
       print(f"{ticker} last logic time not updated")
    else:
        print(f"{ticker} last logic time updated") 