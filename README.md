# algohk2.0

## Project Progress

- Need to reset password / findout password = admin/adminpass
- Check Purchase Lifecycle Function
- Purchase Trail Function
- Interface with Go / Other Python
- Backtest
- Deploy

## Function of Python Script
1. Load History Data from Mongo (Trigger by Cronjob download + Kafka)
2. Check Logic (Premarket)
3. Execute Trade (Purchase)
4. Monitor Trade
5. Handle PT/SL/HD
6. Record Statistics

## View List

| Function          | url                                     | methods | parameters                                       |
| ----------------- | --------------------------------------- | ------- | ------------------------------------------------ |
| get ticker list   | /ticker                                 | GET     | None                                             |
| add ticker for IB | /ticker/add/\<secType>/\<market>/\<symbol> | GET     | symbol = AAPL / market = US / instructment = STK |
|                   |                                         |         |                                                  |

## API List

| Function             | url                                                            | methods | parameters |
| -------------------- | -------------------------------------------------------------- | ------- | ---------- |
| get ticker list      | /api/ticker_list                                               | GET     | None       |
| get orders           | /api/fetch_orders                                              | GET     | None       |
| fetch position       | /api/fetch_positions                                           | GET     | None       |
| fetch account status | /api/fetch_account_status                                      | GET     | None       |
| Place Order          | /api/place_order/\<secType>/\<symbol>/\<action>/\<int:qty>/\<price> | GET     | None       |
| Cancel Order         | /api/cancel_order/\<int:order_id>                               | GET     | None       |
| fetch_execution      | /api/fetch_execution                                           | GET     | None       |

## API Testing Link
```

# Place Order
http://localhost:8080/api/place_order/STK/AAPL/BUY/1/193.2

# Fetch Orders



```

## Initialize the project

### Install Python Dependencies

```
pip install -r requirements.txt
```

### Set up docker containers

```
docker-compose up -d
```

### Start IB API

- Live Trading Port 4001
- Paper Trading Port 4002

### Set up Flask API

```
python server.py
```
