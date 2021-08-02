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
    # user = {'username': 'MLB Players Project'}
    # cursor = mysql.get_db().cursor()
    # cursor.execute('SELECT * FROM tblMlbPlayersImport')
    # result = cursor.fetchall()
    # return render_template('index.html', title='Home', user=user, players=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)