from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


app = Flask(__name__)
app.config.from_object('config.Config')

mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    return "Basic Test"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)