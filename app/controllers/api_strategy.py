from app import app
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app.models.ticker import Strategy, Strategy_list
from datetime import datetime
@app.route('/api/strategy', methods = ['POST'])
def get_stategy():
    strategy = request.form.get("strategy")
    strategies = Strategy.objects(strategy = strategy).all()
    result_dict = {}
    for strategy in strategies:
        result_dict.update(strategy.to_dict())
    return jsonify(result_dict)

@app.route('/api/get_open_position_time', methods=["POST"])
def get_open_position_time():
    strategy = request.form.get("strategy")
    ticker = request.form.get("ticker")
    strategy_tick = Strategy.objects(strategy=strategy, ticker=ticker).first()
    return jsonify(strategy_tick.get_open_position_time())

@app.route('/api/get_open_qty', methods=["POST"])
def get_open_qty():
    strategy = request.form.get("strategy")
    ticker = request.form.get("ticker")
    strategy_tick = Strategy.objects(strategy=strategy, ticker=ticker).first()
    return jsonify(strategy_tick.get_open_qty())

@app.route('/api/get_open_price', methods=["POST"])
def get_open_price():
    strategy = request.form.get("strategy")
    ticker = request.form.get("ticker")
    strategy_tick = Strategy.objects(strategy=strategy, ticker=ticker).first()
    return jsonify(strategy_tick.get_open_price())

@app.route('/api/update_order_execution', methods=['POST'])
def update_order_execution():
    strategy = request.form.get("strategy")
    ticker = request.form.get("ticker")
    open_qty = int(float(request.form.get("open_qty")))
    open_price = float(request.form.get("open_price"))
    strategy_tick = Strategy.objects(strategy=strategy, ticker=ticker).first()
    strategy_tick.open_position_time = datetime.now()
    strategy_tick.open_price = open_price
    strategy_tick.quantity = open_qty
    strategy_tick.save()
    return jsonify({"RET":"OK"})


@app.route("/api/update_strategy_state", methods=["POST"])
def update_strategy_state():
    strategy = request.form.get("strategy")
    ticker = request.form.get("ticker")
    state = request.form.get("state")
    strategy_tick = Strategy.objects(strategy=strategy, ticker=ticker).first()
    strategy_tick.state = state
    strategy_tick.save()
    return jsonify({"RET":"OK"})

@app.route("/api/update_orderId", methods=["POST"])
def update_orderId():
    strategy = request.form.get("strategy")
    ticker = request.form.get("ticker")
    orderId = request.form.get("orderId")
    strategy_tick = Strategy.objects(strategy=strategy, ticker=ticker).first()
    strategy_tick.orderId = orderId
    strategy_tick.save()
    return jsonify({"RET":"OK"})

@app.route('/api/get_orderId', methods=["POST"])
def get_orderId():
    strategy = request.form.get("strategy")
    ticker = request.form.get("ticker")
    strategy_tick = Strategy.objects(strategy=strategy, ticker=ticker).first()
    return jsonify(strategy_tick.get_orderId())

@app.route('/api/update_logic_time', methods=["POST"])
def update_logic_time():
    strategy = request.form.get("strategy")
    ticker = request.form.get("ticker")
    strategy_tick = Strategy.objects(strategy=strategy, ticker=ticker).first()
    strategy_tick.last_logic_time = datetime.now()
    strategy_tick.save()
    return jsonify({"RET":"OK"})