from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.users_model import Users
from flask_app.models.movers_model import Movers
from flask_bcrypt import Bcrypt
import requests
import pandas as pd

bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/register', methods = ['POST'])
def register_info():
    if not Users.validate(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password' : hashed_pw
    }
    session['login_id'] = Users.register_user(data)
    return redirect('/dashboard')


@app.route('/login', methods = ['POST'])
def login_info():
    data = {
        'email' : request.form['login_email']
    }
    user_from_db = Users.check_email(data)
    if not user_from_db:
        flash("Invalid credentials", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_from_db.password, request.form['login_password']):
        flash("Invalid credentials", "log")
        return redirect('/')
    session['login_id'] = user_from_db.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    del session['login_id']
    return redirect('/')


@app.route('/dashboard')
def todays_movers():
    if not "login_id" in session:
        return redirect('/')

    sp500_api = 'https://api.tdameritrade.com/v1/marketdata/$SPX.X/movers'
    sp500_params = {
        'apikey' : 'AO4GMA6ZKRXWCUYQUMHRWI61MAE6ZAE6',
        'direction' : 'up',
        'change': 'percent'
    } 
    sp500_content = requests.get(url = sp500_api, params = sp500_params)
    sp500_movers = sp500_content.json()

    nasdaq_api = 'https://api.tdameritrade.com/v1/marketdata/$COMPX/movers'
    nasdaq_params = {
        'apikey' : 'AO4GMA6ZKRXWCUYQUMHRWI61MAE6ZAE6',
        'direction' : 'up',
        'change': 'percent'
    } 
    nasdaq_content = requests.get(url = nasdaq_api, params = nasdaq_params)
    nasdaq_movers = nasdaq_content.json()

    dow_api = 'https://api.tdameritrade.com/v1/marketdata/$DJI/movers'
    dow_params = {
        'apikey' : 'AO4GMA6ZKRXWCUYQUMHRWI61MAE6ZAE6',
        'direction' : 'up',
        'change': 'percent'
    } 
    dow_content = requests.get(url = dow_api, params = dow_params)
    dow_movers = dow_content.json()
    return render_template('dashboard.html', sp500_movers = sp500_movers, nasdaq_movers = nasdaq_movers, dow_movers = dow_movers)



@app.route('/search', methods = ['POST'])
def search():
    if 'stock_search' in session:
        del session['stock_search']

    stock_search_info = request.form
    session['stock_search'] = stock_search_info
    return redirect('/stock_info')


@app.route('/stock_info')
def stock_info():
    if not "login_id" in session:
        return redirect('/')

    search_api = 'https://api.tdameritrade.com/v1/instruments'
    search_param = {
        'apikey' : 'AO4GMA6ZKRXWCUYQUMHRWI61MAE6ZAE6',
        'symbol' : session['stock_search']['search_stock'],
        'projection' : 'fundamental',
        }
    search_info = requests.get(url = search_api, params = search_param)
    search_data = search_info.json()
    stock_symbol = session['stock_search']['search_stock']
    history_data_info = search_data[stock_symbol]
    history_data = search_data[stock_symbol]['fundamental']

    instant_api = r'https://api.tdameritrade.com/v1/marketdata/{}/quotes'.format(session['stock_search']['search_stock'])
    instant_param = {
        'apikey' : 'AO4GMA6ZKRXWCUYQUMHRWI61MAE6ZAE6'
        }
    current_data = requests.get(url = instant_api, params = instant_param)
    todays_data = current_data.json()
    live_data = todays_data[stock_symbol]

    history_api = r'https://api.tdameritrade.com/v1/marketdata/{}/pricehistory'.format(session['stock_search']['search_stock'])
    history_param = {
        'apikey' : 'AO4GMA6ZKRXWCUYQUMHRWI61MAE6ZAE6',
        'periodType' : 'day',
        'frequencyType' : 'minute',
        'frequency' : '1',
        'period' : '1',
        'needExtendedHoursData' : 'false'
        }
    history_content = requests.get(url = history_api, params = history_param)
    stock_history = history_content.json()

    return render_template('stock_info.html', history_data = history_data, history_data_info = history_data_info, live_data = live_data, search_data = search_data)
