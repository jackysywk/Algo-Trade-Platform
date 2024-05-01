from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app.models.ticker import Ticker 


@app.route('/ticker', methods = ['GET'])
@login_required
def ticker():
    tickers = Ticker.objects()
    tickers = [ticker.to_dict() for ticker in tickers]
    return render_template('ticker.html', tickers = tickers)

@app.route('/ticker/add/', methods = ['POST'])
def add_ticker():
    secType = request.form.get('secType')
    primaryExchange = request.form.get("primaryExchange")
    market = request.form.get('market')
    ticker = request.form.get('ticker')
    if primaryExchange:
        new_ticker = Ticker(ticker = ticker,
                            market = market,
                            secType = secType,
                            primaryExchange=primaryExchange)
    else:
                new_ticker = Ticker(ticker = ticker,
                            market = market,
                            secType = secType)
    new_ticker.save()

    return {'status':'OK'}
