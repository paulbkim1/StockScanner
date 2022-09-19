from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.watchlists_model import Watchlists

@app.route('/watchlist/add')
def watchlist_add():
    add_to_watchlist = Watchlists.check_watchlist(session['stock_search']['search_stock'])
    if not add_to_watchlist:
        flash("Equity already in watchlist", "watchlist")
        return redirect('/stock_info')
    data = {
        'user_id' : session['login_id'],
        'symbol' : session['stock_search']['search_stock']
    }
    Watchlists.add_watchlist(data)
    return redirect('/stock_info')

@app.route('/watchlist')
def watchlist_page():
    current_watchlist = Watchlists.view_watchlist(session['login_id'])
    return render_template('watchlist.html', current_watchlist = current_watchlist)