from crypt import methods
from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.movers_model import Movers
import requests
import pandas as pd
import time

# @app.route('/stocks_on_the_move')
# def stocks_otm():
#     if not "login_id" in session:
#         return redirect('/')
#     data = {
#         'user_id' : session['login_id']
#     }
#     list_of_movers = Movers.movers_list(data)
#     return render_template('stocks_otm.html', list_of_movers = list_of_movers)


# @app.route('/add_comments', methods = ['POST'])
# def add_comments():
#     data = {
#         **request.form
#     }
#     Movers.add_comment(data)
#     return redirect('/stocks_on_the_move')

# @app.route('/delete_comments/<int:id>')
# def delete_comments(id):
#     data = {
#         'id' : id
#     }
#     Movers.delete_comment(data)
#     return redirect('/stocks_on_the_move')

@app.route('/link/search/<symbol>')
def link_search(symbol):
    if 'stock_search' in session:
        del session['stock_search']

    data = {
        'search_stock' : symbol
    }
    session['stock_search'] = data
    return redirect('/stock_info')

# def algo():
#     starttime = time.time()
#     list = []
#     while True:
#         df = pd.read_excel('/Users/paulkim/Desktop/Stocks_list.xlsx')
#         symbols = df['Symbol'].values.tolist()
#         start = 0
#         if start > 6890:
#             start = 0
#         end = 150
#         if end > 7000:
#             end = 150
#         algo_api = 'https://api.tdameritrade.com/v1/marketdata/quotes'
#         while start < len(symbols):
#             tickers = symbols[start:end]
#             algo_param = {
#                 'apikey' : 'AO4GMA6ZKRXWCUYQUMHRWI61MAE6ZAE6',
#                 'symbol' : tickers,
#             }
#             start = end
#             end+= 150
#             current_data = requests.get(url = algo_api, params = algo_param)
#             algo_data = current_data.json()
#             for i in algo_data:
#                 if algo_data[i]['openPrice'] > 0:
#                     if ((algo_data[i]['lastPrice'] - algo_data[i]['openPrice']) / algo_data[i]['openPrice']) > .05:
#                         if algo_data[i]['totalVolume'] > 700000:
#                             if algo_data[i]['lastPrice'] > 1.10 and algo_data[i]['lastPrice'] < 150.00:
#                                 if algo_data[i]['bidSize'] > 1000:
#                                     if algo_data[i]['volatility'] > .2:
#                                         if ((algo_data[i]['lastPrice'] - algo_data[i]['highPrice']) / algo_data[i]['highPrice']) > -0.10:
#                                             if ((algo_data[i]['lastPrice'] - algo_data[i]['lowPrice']) / algo_data[i]['lowPrice']) > 0.10:
#                                                 data = {
#                                                     'symbol' : i
#                                                 }
#                                                 check_symbol = Movers.check_mover(data)
#                                                 if check_symbol == False:
#                                                     movers_api = r'https://api.tdameritrade.com/v1/marketdata/{}/quotes'.format(i)
#                                                     movers_param = {
#                                                         'apikey' : 'AO4GMA6ZKRXWCUYQUMHRWI61MAE6ZAE6'
#                                                     }
#                                                     movers_data = requests.get(url = movers_api, params = movers_param)
#                                                     movers_otm = movers_data.json()
#                                                     add_movers_data = {
#                                                         'symbol' : movers_otm[i]['symbol'],
#                                                         'price' : movers_otm[i]['lastPrice'],
#                                                         'volume' : movers_otm[i]['totalVolume'],
#                                                         'user_id' : session['login_id']
#                                                     }
#                                                     list.append(add_movers_data)
#                                                     Movers.add_mover(add_movers_data)
#         print(list)
#         time.sleep(60.0 - ((time.time() - starttime) % 60.0))