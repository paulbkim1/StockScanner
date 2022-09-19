from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users_model

class Watchlists:
    def __init__(self, data):
        self.id = data['id']
        self.symbol = data['symbol']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def check_watchlist(cls,data):
        query = "SELECT * FROM watchlists WHERE symbol = %(data)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results == True:
            return False

    @classmethod
    def add_watchlist(cls,data):
        query = "INSERT INTO watchlists (symbol, user_id) VALUES ('symbol', 'user_id');"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def view_watchlist(cls,data):
        query = "SELECT symbol FROM watchlists JOIN users ON users.id = user_id WHERE user_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query)
        if len(results) > 0:
            all_watchlists = []
            for i in results:
                this_watchlist = cls(i)
                user_data = {
                    **i,
                    'id' : i['users.id'],
                    'created_at' : i['users.created_at'],
                    'updated_at' : i['users.updated_at']
                }
                this_watchlist = users_model.Users(user_data)
                this_watchlist.planner = this_watchlist
                all_watchlists.append(this_watchlist)
            return all_watchlists
        return []