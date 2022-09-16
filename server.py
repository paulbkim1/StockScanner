from flask_app import app
from flask_app.controllers import movers_controller
from flask_app.controllers import users_controller
from flask_app.controllers import watchlist_controller



if __name__=="__main__":
    app.run(debug=True)