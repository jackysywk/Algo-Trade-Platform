from flask_login import UserMixin
from mongoengine import Document, StringField, CASCADE, BooleanField


class Ticker(Document):
    meta = {'collection': 'tickers'}
    ticker = StringField(required=True)
    market = StringField(required=True)
    instrument = StringField(required=True)

    def to_dict(self):
        return {"id":str(self.id),
                "ticker": self.ticker,
                "market": self.market,
                "instrument": self.instrument,
                }