from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL

class Watchlists:
    def __init__(self, data):
        self.id = data['id']
        self.symbol = data['symbol']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def check_watchlist(cls,data):
        query = "SELECT * FROM watchlists WHERE symbol = %(symbol)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) > 0:
            return True
        return False

    @classmethod
    def add_watchlist(cls,data2):
        query = "INSERT INTO watchlists (symbol, user_id) VALUES (%(symbol)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data2)

    @classmethod
    def view_watchlist(cls,data):
        query = 'SELECT symbol FROM watchlists WHERE user_id = %(user_id)s;'
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) > 0:
            return results

    @classmethod
    def delete_watchlist(cls,data):
        query = "DELETE FROM watchlists WHERE symbol = %(symbol)s;"
        return connectToMySQL(DATABASE).query_db(query,data)