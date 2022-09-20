from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.watchlists_model import Watchlists
import requests
import pandas as pd

@app.route('/stocks_on_the_move')
def stocks_otm():
    if not "login_id" in session:
        return redirect('/')
    return render_template('stocks_otm.html')

@app.route('/dashboards')
def algo():
    df = pd.read_excel('/Users/paulkim/Desktop/Stocks_list.xlsx')
    symbols = df['Symbol'].values.tolist()
    start = 0
    end = 150
    final = []
    algo_api = 'https://api.tdameritrade.com/v1/marketdata/quotes'
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
        # final.append(algo_data)
        for i in algo_data:
            if algo_data[i]['netChange'] > .10:
                if algo_data[i]['totalVolume'] > 1000000:
                    if algo_data[i]['lastPrice'] > 1.10 and algo_data[i]['lastPrice'] < 150.00:
                        if algo_data[i]['bidSize'] > 1000:
                            if algo_data[i]['volatility'] > .2:
                                if (algo_data[i]['lastPrice'] + .10) > algo_data[i]['openPrice']:
                                    final.append(i)
    print(final)
    print(len(final))
