from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"
DATABASE = 'stocks_db'