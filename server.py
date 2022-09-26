from flask_app import app
from flask_app.controllers import movers_controller
from flask_app.controllers import users_controller
from flask_app.controllers import watchlist_controller
from threading import Thread



if __name__=="__main__":
    # Thread(target = movers_controller.algo).start()
    app.run(debug=True)