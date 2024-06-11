from app import app
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app.models.ticker import Strategy, Strategy_list

@app.route('/api/strategy/<strategy>', methods = ['GET'])
def get_stategy(strategy):
    strategies = Strategy.objects(strategy = strategy).all()
    result_dict = {}
    for strategy in strategies:
        result_dict.update(strategy.to_dict())
    return result_dict