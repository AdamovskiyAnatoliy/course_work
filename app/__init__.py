import cx_Oracle
from flask import Flask
from config import Config


app = Flask(__name__)
config = Config()

app.secret_key = config.SECRET_KEY
app.jinja_env.globals.update(zip=zip, type=type, list=list, str=str)


from app import routes
