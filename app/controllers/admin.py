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

@app.route('/ticker/add/<secType>/<market>/<symbol>', methods = ['GET'])
@login_required
def add_ticker(secType, market, symbol):
    new_ticker = Ticker(ticker = symbol,
                        market = market,
                        instrument = secType)
    new_ticker.save()

    return redirect(url_for('ticker'))
