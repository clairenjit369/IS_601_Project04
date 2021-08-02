"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:

    # General Config
    SECRET_KEY = "IHUGVFIYUJYIGUibt6gh"
    FLASK_APP = "development"
    FLASK_ENV = "app.py"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

    # Database Config
    MYSQL_DATABASE_HOST = environ.get('MYSQL_DATABASE_HOST')
    MYSQL_DATABASE_USER = environ.get('MYSQL_DATABASE_USER')
    MYSQL_DATABASE_PASSWORD = environ.get('MYSQL_DATABASE_PASSWORD')
    MYSQL_DATABASE_PORT = int(environ.get('MYSQL_DATABASE_PORT'))
    MYSQL_DATABASE_DB = environ.get('MYSQL_DATABASE_DB')

    # Static Assets and Templates
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
