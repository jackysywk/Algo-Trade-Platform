from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app.models.ticker import Ticker 
from app.models.ib_interface import create_contract, create_order
from ibapi.execution import ExecutionFilter
import asyncio
import time
from datetime import datetime
from app.models.account import Order_history
@app.route('/api/ticker_list', methods = ['GET'])
def api_ticker():
    tickers = Ticker.objects()
    tickers = [ticker.to_dict() for ticker in tickers]
    return jsonify(tickers)


@app.route('/api/fetch_orders', methods=['GET'])
async def fetch_orders():
    #connect_to_ib()
    app.ib_api.orders = []  # Clear previous orders
    app.ib_api.reqOpenOrders()  # Request list of open orders
    await asyncio.sleep(0.5)
    return jsonify(app.ib_api.orders)

@app.route('/api/fetch_positions', methods=['GET'])
async def fetch_positions():
    #connect_to_ib()
    app.ib_api.positions = []  # Clear previous positions
    app.ib_api.reqPositions()  # Request list of current positions
    #disconnect_from_ib()
    await asyncio.sleep(0.5)
    return jsonify(app.ib_api.positions)

@app.route('/api/fetch_account_status', methods=['GET'])
async def fetch_account_status():
    #connect_to_ib()
    app.ib_api.account_values = {}  # Clear previous account values
    app.ib_api.reqAccountUpdates(True, '')  # Request account updates
    #disconnect_from_ib()
    await asyncio.sleep(0.5)
    return jsonify(app.ib_api.account_values)

@app.route('/api/place_order/<secType>/<symbol>/<action>/<int:qty>/<price>', methods=['GET'])
def place_order( secType, symbol, action, qty, price):
    price = float(price)
    contract = create_contract(symbol=symbol, secType = secType)
    order = create_order(action=action,qty=qty,price=price)
    # Make sure nextOrderId is ready
    print(app.ib_api.nextOrderId)
    if app.ib_api.nextOrderId is None:
        print("Requesting the next order id")
        app.ib_api.reqIds(1)  # Request next valid order ID

        time.sleep(2)  # Simple way to wait for the server to respond

    if app.ib_api.nextOrderId is not None:
        app.ib_api.placeOrder(app.ib_api.nextOrderId, contract, order)
        app.ib_api.nextOrderId += 1  # Increment the nextOrderId
        return jsonify({"status": "Order placed", "orderId": app.ib_api.nextOrderId - 1})
    
    else:
        return jsonify({"status": "Error", "message": "Could not retrieve next order ID"})
    
@app.route('/api/cancel_order/<int:order_id>', methods=['GET'])
async def cancel_order( order_id):
    app.ib_api.cancelOrder(order_id)
    await asyncio.sleep(0.5)
    return redirect(url_for("fetch_orders"))

@app.route('/api/fetch_execution', methods=['GET'])
async def fetch_execution():
    app.ib_api.execution = []  # Clear previous account values
    exec_filter = ExecutionFilter()
    app.ib_api.reqExecutions(1, exec_filter)
    await asyncio.sleep(0.5)
    return jsonify(app.ib_api.execution)