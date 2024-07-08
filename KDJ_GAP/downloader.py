import yfinance as yf
import sys
sys.path.append('app')
import os
import requests
import time
def get_strategy_profile(strategy_name):
    form_data = {
        "strategy":strategy_name
    }
    strategy_dict = requests.post("http://localhost:8080/api/strategy", data = form_data).json()
    ticker_list = list(strategy_dict.keys())
    return ticker_list
if __name__ == "__main__":
    # Get the directory containing the script
    now_path = os.path.dirname(os.path.abspath(__file__))

    # Get the name of the directory containing the script
    strategy_name = os.path.basename(now_path)

    tickers = get_strategy_profile(strategy_name)

    for ticker in tickers:
        df = yf.Ticker(ticker).history('2y')
        time.sleep(0.1)
        df.reset_index()
        print(df.tail(3))
        df.to_csv(f'{now_path}/data/{ticker}.csv', encoding='utf-8')