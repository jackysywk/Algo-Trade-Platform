from mongoengine import Document, StringField, IntField, DateTimeField, DateField, FloatField


class Order_history(Document):
    meta = {'collection': 'order_history'}
    strategy = StringField(required=True)
    ticker = StringField(required=True)
    quantity = IntField(required=True)
    open_price = FloatField(required=True)
    open_datetime = DateTimeField(required=True)
    close_price = FloatField(required=True)
    close_datetime = DateTimeField(required=True)
    status = StringField(required=True)
    message = StringField(required=True)

    def to_dict(self):
        return {"id":str(self.id),
                "strategy": self.strategy,
                "ticker": self.ticker,
                "quantity": self.quantity,
                "open_price": self.open_price,
                "open_datetime":self.open_datetime,
                "close_price":self.close_price,
                "close_datetime":self.close_datetime,
                "status":self.status,
                "message":self.message
                }

class Stock_equity_value(Document):
    meta={'collection':'stock_equity_value'}
    date = DateField(required=True)
    strategy = StringField(required=True)
    stock = StringField(required=True)
    unit_price = FloatField(required=True)
    amount = FloatField(required=True)

class Account_equity_value(Document):
    meta = {'collection':'account_equity_value'}
    date = DateField(required=True)
    account = StringField(required=True)
    equity_value = FloatField(required=True)