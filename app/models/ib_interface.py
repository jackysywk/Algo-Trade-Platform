from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.order import Order
from ibapi.contract import Contract
import threading
import time
from mongoengine import Document, IntField, DateTimeField
from app import app

class LastOrderId(Document):
    meta = {'collection': 'LastOrder'}
    OrderId = IntField(required=True)
    Date = DateTimeField()

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.orders = []
        self.positions = []
        self.account_values = {}
        self.nextOrderId = None  # Initialize nextOrderId

    def nextValidId(self, orderId: int):
        # This callback receives the next valid order ID
        self.nextOrderId = orderId
        print("The next valid order ID is:", self.nextOrderId)

    def openOrder(self, orderId, contract, order, orderState):
        # Called for each open order, you might customize what info to store
        self.orders.append({
            "orderId": orderId,
            "symbol": contract.symbol,
            "action": order.action,
            "quantity": order.totalQuantity,
            "orderType": order.orderType,
            "limitPrice": order.lmtPrice,
            "status": orderState.status
        })

    def position(self, account, contract, position, avgCost):
        # Called for each position in the account
        self.positions.append({
            "account": account,
            "symbol": contract.symbol,
            "position": position,
            "avgCost": avgCost
        })

    def openOrderEnd(self):
        # Indicates the end of the initial open orders snapshot
        print("Received all open orders.")

    def positionEnd(self):
        # Indicates the end of the positions snapshot
        print("Received all positions.")
    def updateAccountValue(self, key, val, currency, accountName):
            self.account_values[key] = {"value": val, "currency": currency}

    def accountDownloadEnd(self, accountName):
        # Indicates the end of the account details snapshot
        print("Received all account data for account:", accountName)
    def on_error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def on_order_status(self, orderId, status, filled, remaining, avgFillPrice, permId,
                        parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print("OrderStatus. Id:", orderId, "Status:", status, "Filled:", filled,
              "Remaining:", remaining, "AvgFillPrice:", avgFillPrice,
              "PermId:", permId, "ParentId:", parentId, "LastFillPrice:",lastFillPrice,
              "ClientId:", clientId, "WhyHeld:", whyHeld, "MktCapPrice:", mktCapPrice)

def run_loop():
    app.ib_api.run()

def connect_to_ib():
    app.ib_api = IBapi()
    app.ib_api.connect('127.0.0.1', 4002, 123)
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()
    time.sleep(1)  # Allow time for connection to establish

def disconnect_from_ib():
    time.sleep(3)  # Allow time for responses
    app.ib_api.disconnect()

def create_contract(symbol, secType="STK", currency="USD"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = "SMART"
    contract.currency = currency
    return contract

def create_order(action, qty, price, orderType ="LIMIT"):
    # Example order details (customize according to your requirements)
    order = Order()
    order.action = action
    order.totalQuantity = qty
    order.orderType = orderType
    order.lmtPrice = price
    order.eTradeOnly=False
    order.firmQuoteOnly=False
    return order