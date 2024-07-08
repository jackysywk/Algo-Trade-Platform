from kafka import KafkaConsumer
import sys
sys.path.append("../utils")
sys.path.append('../')
import json
from log_utils import setup_logger
from datetime import datetime, time, timedelta
global strategy_name

from dummy import Dummy
from strategy.strategy import bid_ask_isvalid, update_last_logic_time, make_purchase_order, make_sell_order, check_pt_sl, check_holding_days, get_orderId, update_orderId, check_execution, get_order_qty
dummy_instance = Dummy()
strategy_name = dummy_instance.strategy_name
dummy_instance.get_strategy_profile()

logger = setup_logger(strategy_name, log_dir = '../log', log_file = f'{strategy_name}.log')

if __name__ == "__main__":
    # print("Program Start")
    logger.info(f'{strategy_name} strategy started')
    print(f'{strategy_name} strategy started')
    bid_ask_dict = dummy_instance.get_bid_ask_dict()
    while True:
        consumer = KafkaConsumer(
            bootstrap_servers= "localhost:9092",
            value_deserializer = lambda v:json.loads(v.decode('utf-8')),
        )
        consumer.subscribe(dummy_instance.ticker_list)

        #logger.info(f'{strategy_name} Consumer Started')
        print("channel subscribed")
        for message in consumer:
            message_key = message.key.decode()
            if dummy_instance.profile[message.topic]['state'] == 'Monitoring Signal':
                format_str = '%Y-%m-%dT%H:%M:%S.%f'
                logic_time = datetime.strptime(dummy_instance.profile[message.topic]['last_logic_time'], format_str)
                if datetime.now().date() > logic_time.date():

                    # Checking the state of the trading time.
                    if dummy_instance.profile[message.topic]['parameters']['trade_time'] == 'morning':
                        #if (time(9,30) <= datetime.now().time()) and (datetime.now().time()<= time(9,35)):
                        if True:
                            trade_logic = dummy_instance.check_trade_logic(dummy_instance.profile[message.topic])
                            update_last_logic_time(strategy_obj=dummy_instance.profile[message.topic])
                            dummy_instance.profile[message.topic]['last_logic_time'] = datetime.now().strftime(format_str)
                    if dummy_instance.profile[message.topic]['parameters']['trade_time'] == 'afternoon':
                        #if (time(15,50) <= datetime.now().time()) and (datetime.now().time()<= time(16,00)):
                        if True:
                            trade_logic = dummy_instance.check_trade_logic(dummy_instance.profile[message.topic])
                            update_last_logic_time(strategy_obj=dummy_instance.profile[message.topic])
                            dummy_instance.profile[message.topic]['last_logic_time'] = datetime.now().strftime(format_str)
                    if trade_logic:
                        dummy_instance.profile[message.topic]['state'] = "Signal Detected"
                        dummy_instance.update_ticker_state(message.topic, 'Signal Detected')

            elif dummy_instance.profile[message.topic]['state'] == 'Strategy Stopped':
                pass
            elif dummy_instance.profile[message.topic]['state'] == 'Signal Detected':
                if bid_ask_isvalid(bid_ask_dict, message.topic):
                    quantity = 1
                    print("Bid ask dict ready")
                    res = make_purchase_order(dummy_instance.profile[message.topic], 
                                        quantity, 
                                        bid_ask_dict[message.topic]['ask'])
                    if res['status'] == "Order placed":
                        orderId = res['orderId']
                    update_orderId(strategy_obj=dummy_instance.profile[message.topic], 
                                   orderId=orderId)
                    dummy_instance.profile[message.topic]['state'] = "Opening Order"
                    dummy_instance.update_ticker_state(message.topic, 'Opening Order')
                else:
                    if message_key == "bid":
                        #print('updating bid')
                        bid_ask_dict[message.topic]['bid'] = message.value["price"]
                        bid_ask_dict[message.topic]['bid_timestamp'] = datetime.now()
                    elif message_key == 'ask':
                        #print('updating_ask')
                        bid_ask_dict[message.topic]['ask'] = message.value["price"]
                        bid_ask_dict[message.topic]['ask_timestamp'] = datetime.now()
                    elif message_key == 'last_price':
                        #print('updating_last_price')
                        bid_ask_dict[message.topic]['last_price'] = message.value["price"]
                        bid_ask_dict[message.topic]['last_price_timestamp'] = datetime.now()
            elif dummy_instance.profile[message.topic]['state'] == 'Opening Order':
                status, orderId = get_orderId(strategy_obj=dummy_instance.profile[message.topic])
                if status:
                    order_status, execId = check_execution(strategy_obj = dummy_instance.profile[message.topic],
                                                        orderId = orderId)
                    if order_status:
                        print(f"{message.topic} order executed")
                        dummy_instance.profile[message.topic]['state'] = "Open Position"
                        dummy_instance.update_ticker_state(message.topic, 'Open Position')
                else:
                    print(message.topic,'has problem')
                    pass
                
            elif dummy_instance.profile[message.topic]['state'] == 'Open Position':
                #print(f"{message.topic} position opened")
                if bid_ask_isvalid(bid_ask_dict, message.topic):
                    sell_logic=False
                    sell_message = ""
                    #check holding day logic between 1545 and 1600
                    if (time(15,45) > datetime.now().time()) and (time(16,00) < datetime.now().time()):
                        sell_logic, sell_message = check_holding_days(dummy_instance.profile[message.topic])
                        
                    #check PTSL
                    if message_key == 'last_price' and dummy_instance.resolution=='realtime':
                        last_price = message.value["price"]
                        sell_logic, sell_message = check_pt_sl(dummy_instance.profile[message.topic],last_price)
                    elif message_key == 'last_price' and dummy_instance.resolution=='daily':
                        last_price = message.value["price"]
                        if (time(15,45) > datetime.now().time()) and (time(16,00) < datetime.now().time()):
                            sell_logic, sell_message = check_pt_sl(dummy_instance.profile[message.topic],last_price)

                    if sell_logic:
                        status, qty = get_order_qty(strategy_obj=dummy_instance.profile[message.topic])
                        if status:
                            res = make_sell_order(profile = dummy_instance.profile[message.topic],
                                            qty = qty,
                                            price = bid_ask_dict[message.topic]['bid'])
                            if res['status'] == "Order placed":
                                orderId = res['orderId']
                            update_orderId(strategy_obj=dummy_instance.profile[message.topic], 
                                        orderId=orderId)
                            dummy_instance.profile[message.topic]['state'] = "Selling Order"
                            dummy_instance.update_ticker_state(message.topic, 'Selling Order')
                        else:
                            print("API Error")
                else:
                    if message_key == "bid":
                        #print('updating bid')
                        bid_ask_dict[message.topic]['bid'] = message.value["price"]
                        bid_ask_dict[message.topic]['bid_timestamp'] = datetime.now()
                    elif message_key == 'ask':
                        #print('updating_ask')
                        bid_ask_dict[message.topic]['ask'] = message.value["price"]
                        bid_ask_dict[message.topic]['ask_timestamp'] = datetime.now()
                    elif message_key == 'last_price':
                        #print('updating_last_price')
                        bid_ask_dict[message.topic]['last_price'] = message.value["price"]
                        bid_ask_dict[message.topic]['last_price_timestamp'] = datetime.now()
            elif dummy_instance.profile[message.topic]['state'] == 'Selling Order':
                status, orderId = get_orderId(strategy_obj=dummy_instance.profile[message.topic])
                if status:
                    order_status, execId = check_execution(strategy_obj = dummy_instance.profile[message.topic],
                                                        orderId = orderId)
                    if order_status:
                        print(f"{message.topic} order executed")
                        dummy_instance.profile[message.topic]['state'] = "Monitoring Signal"
                        dummy_instance.update_ticker_state(message.topic, 'Monitoring Signal')
                else:
                    print(message.topic,'has problem')
                    pass