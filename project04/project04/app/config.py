"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    MYSQL_DATABASE_HOST = environ.get('MYSQL_DATABASE_HOST')
    MYSQL_DATABASE_USER = environ.get('MYSQL_DATABASE_USER')
    MYSQL_DATABASE_PASSWORD = environ.get('MYSQL_DATABASE_PASSWORD')
    MYSQL_DATABASE_PORT = environ.get('MYSQL_DATABASE_PORT')
    MYSQL_DATABASE_DB = environ.get('MYSQL_DATABASE_DB')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
