from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL

class Movers:
    def __init__(self,data):
        self.id = data['id']
        self.symbol = data['symbol']
        self.price = data['price']
        self.volume = data['volume']
        self.comments = data['comments']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def check_mover(cls,data):
        query = 'SELECT * FROM movers WHERE symbol = %(symbol)s;'
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) > 1:
            return True
        return False

    @classmethod
    def add_mover(cls,data):
        query = 'INSERT INTO movers (symbol, price, volume, user_id) VALUES (%(symbol)s, %(price)s, %(volume)s, %(user_id)s);'
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def movers_list(cls,data):
        query = 'SELECT * FROM movers WHERE user_id = %(user_id)s ORDER BY created_at DESC;'
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) > 0:
            all_movers = []
            for i in results:
                this_mover = cls(i)
                all_movers.append(this_mover)
            return all_movers

    @classmethod
    def add_comment(cls,data):
        query = "UPDATE movers SET comments = %(comments)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def delete_comment(cls,data):
        query = "DELETE FROM movers WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)