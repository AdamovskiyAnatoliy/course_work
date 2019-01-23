import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_name'
    USER_NAME = 'my_name'
    PASSWORD = 'my_name'
    SERVER = 'xe'
