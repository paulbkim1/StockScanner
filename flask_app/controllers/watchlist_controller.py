from crypt import methods
from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.watchlists_model import Watchlists
from flask_app.models.movers_model import Movers
import requests
import pandas as pd
import time

@app.route('/watchlist/add')
def watchlist_add():
    data = {
        'symbol' : session['stock_search']['search_stock']
    }
    add_to_watchlist = Watchlists.check_watchlist(data)
    if add_to_watchlist == True:
        flash("Equity already in watchlist", "watchlist")
        return redirect('/stock_info')
    data2 = {
        'symbol' : session['stock_search']['search_stock'],
        'user_id' : session['login_id'],
    }
    Watchlists.add_watchlist(data2)
    return redirect('/stock_info')

@app.route('/watchlist')
def watchlist_page():
    if not "login_id" in session:
        return redirect('/')

    data = {
        'user_id' : session['login_id']
    }
    current_watchlist = Watchlists.view_watchlist(data)
    watchlists = {}
    for i in current_watchlist:
        instant_api = 'https://api.tdameritrade.com/v1/marketdata/quotes'
        instant_param = {
            'apikey' : 'AO4GMA6ZKRXWCUYQUMHRWI61MAE6ZAE6',
            'symbol' : i['symbol']
            }
        current_data = requests.get(url = instant_api, params = instant_param)
        todays_data = current_data.json()
        watchlists.update(todays_data)
    return render_template('watchlist.html', watchlists = watchlists)


@app.route('/delete_watchlist/<symbol>')
def delete_watchlist(symbol):
    data = {
        'symbol' : symbol
    }
    Watchlists.delete_watchlist(data)
    return redirect('/watchlist')


@app.route('/screener1')
def screener_1():
    if not "login_id" in session:
        return redirect('/')
    return render_template('screener1.html')

@app.route('/screener/search', methods = ['POST'])
def search_screener():
    if "screener_data" in session:
        del session['screener_data']
    parameters = {
        **request.form
    }
    df = pd.read_excel('/Users/paulkim/Desktop/stock_scanner_project/Stocks_list.xlsx')
    symbols = df['Symbol'].values.tolist()
    start = 0
    end = 150
    algo_api = 'https://api.tdameritrade.com/v1/marketdata/quotes'
    screen_data = []
    while start < len(symbols):
        tickers = symbols[start:end]
        algo_param = {
            'apikey' : 'AO4GMA6ZKRXWCUYQUMHRWI61MAE6ZAE6',
            'symbol' : tickers,
        }
        start = end
        end+= 150
        current_data = requests.get(url = algo_api, params = algo_param)
        algo_data = current_data.json()
        for i in algo_data:
            if float(algo_data[i]['lastPrice']) > float(parameters["low_price"]):
                if float(algo_data[i]['lastPrice']) < float(parameters["high_price"]):
                    if int(algo_data[i]['totalVolume']) > int(parameters["low_volume"]):
                        if int(algo_data[i]['totalVolume']) < int(parameters["high_volume"]):
                            if float(algo_data[i]['netChange']) > float(parameters["low_change"]):
                                if float(algo_data[i]['netChange']) < float(parameters["high_change"]):
                                    screen_data.append(algo_data[i])
    session['screener_data'] = screen_data
    return redirect('/screener2')

@app.route('/screener2')
def show_screener_results():
    if not "login_id" in session:
        return redirect('/')
    if not session['screener_data']:
        flash("No equities for those parameters", "param")
    screener_results = session['screener_data']
    return render_template('screener2.html', screener_results = screener_results)