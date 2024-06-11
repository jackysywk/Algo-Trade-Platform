from ibapi.client import EClient
from ibapi.wrapper import EWrapper  
from ibapi.contract import Contract
import threading
import time
from confluent_kafka import Producer
import json
from datetime import datetime
import sys
import requests
sys.path.append('../utils')
from log_utils import setup_logger
logger = setup_logger("IB Producer")
def delivery_report(err, msg):
    if err is not None:
        logger.fatal('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()),datetime.now())

global ticker_dict
ticker_dict={}
global tick_type_dict
tick_type_dict={
	1:"bid",
	2:"ask",
	4:"last_price",
	#6:"day_high",
	#7:"day_low"
}
class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
		self.producer = Producer({"bootstrap.servers":"kafka:9092"})
	def tickPrice(self, reqId, tickType, price, attrib):
		try:
			if tickType in tick_type_dict.keys():
				data={
                    'ticker':ticker_dict[reqId],
                    'tick_type':tick_type_dict[tickType],
                    'price':price
                }
				data_json = json.dumps(data)
				data_json = data_json.encode("utf-8")
				self.producer.poll(0)
				self.producer.produce(topic = ticker_dict[reqId],key=tick_type_dict[tickType], value=data_json,callback=delivery_report)
		except Exception as e:
			logger.fatal(e)
        #if tickType == 2 and reqId == 1:
		#	print('The current ask price is: ', price)
def run_loop():
	app.run()

def get_contract(ticker,secType,primaryExchange=None):
	contract = Contract()
	contract.symbol = ticker
	contract.secType = secType
	contract.exchange = "SMART"
	if primaryExchange:
		contract.primaryExchange = primaryExchange
	contract.currency = 'USD'
	return contract

def get_ticker_list():
	res = requests.get("http://host.docker.internal:8080/api/ticker_list").json()
	print(res)
	return res


if __name__=='__main__':
	#REAL Port = 4001, Fake Port = 4002
	app = IBapi()

	app.connect('host.docker.internal',4002,10)

	api_thread = threading.Thread(target = run_loop, daemon=True)
	api_thread.start()
	time.sleep(1)
	#ticker_list = ['AAPL']
	ticker_list = get_ticker_list()
	for i,ticker in enumerate(ticker_list,1):
		contract = get_contract(ticker=ticker['ticker'],
						  secType=ticker['secType'],
						  primaryExchange=ticker['primaryExchange'])
		ticker_dict[i]=ticker['ticker']
		app.reqMktData(i, contract, '', False, False, [])
		logger.info(f'{ticker["ticker"]} subscription')
	#time.sleep(10) #Sleep interval to allow time for incoming price data
	#app.disconnect()