from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect, render_template, url_for, Blueprint, flash
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

from forms import SignupForm, LoginForm


app = Flask(__name__)
app.config.from_object('config.Config')


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)


mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        # Get User by Email
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM `addresses` WHERE id = %s', user_id)
        result = cursor.fetchall()
        if len(result) != 0:
            my_id = result[0]['id']
            name = result[0]['name']
            email = result[0]['email']
            password = result[0]['password']
            return User(my_id, name, email, password)
        else:
            return None
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


# User authentication is below...
# Sign Up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User sign-up form for account creation."""
    form = SignupForm()
    if form.validate_on_submit():

        # Get Form Fields
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # Get User by Email
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM `addresses` WHERE email = %s', email)
        result = cursor.fetchall()
        if len(result) == 0:  # User does not exist yet
            # Encrypt Password
            hashed_password = generate_password_hash(
                password,
                method='sha256'
            )

            # Add User to DB
            insert_cursor = mysql.get_db().cursor()
            input_data = (name, email, hashed_password)
            sql_insert_query = """INSERT INTO `addresses` (Fname, Lname, email, password) VALUES (%s, %s, %s) """
            insert_cursor.execute(sql_insert_query, input_data)
            mysql.get_db().commit()

            # Add User to session
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM `addresses` WHERE email = %s', email)
            result = cursor.fetchall()
            user_id = result[0]['id']
            user = User(user_id, name, email, hashed_password)
            login_user(user)  # Log in as newly created user
            return redirect('/')
        flash('A user already exists with that email address.')
    return render_template(
        'signup.html',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login form for account creation."""
    form = LoginForm()

    if form.validate_on_submit():

        # Get Form Fields
        email = form.email.data
        password = form.password.data

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Get User by Email and Hashed Password
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM `addresses` WHERE email = %s AND password = %s', (email, hashed_password))
        result = cursor.fetchall()
        if len(result) != 0:  # User found
            # Add User to session
            user_id = result[0]['id']
            name = result[0]['name']
            user = User(user_id, name, email, hashed_password)
            login_user(user)  # Log in as newly created user
            return redirect('/')
        flash('User Not Found! Please re-check email and/or password.')
    return render_template(
        'login.html',
        title='Login to Account.',
        form=form,
        template='login-page',
        body="Login to your account."
    )


# API Endpoints are below...
# View all Players
@app.route('/api/v1/players', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


# View a single Player record by Id
@app.route('/api/v1/player/<int:player_id>', methods=['GET'])
def api_retrieve(player_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses WHERE id=%s', player_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


# Add a New Player
@app.route('/api/v1/player', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    input_data = (content['fld_Name'], content['fld_Team'],
                  content['fld_Position'], content['fld_Age'],
                  content['fld_Height_inches'], content['fld_Weight_lbs'])
    sql_insert_query = """INSERT INTO addresses (fld_Name,fld_Team,fld_Position,fld_Age,fld_Height_inches,fld_Weight_lbs) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, input_data)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


# Update an existing Player by Id
@app.route('/api/v1/player/<int:player_id>', methods=['PUT'])
def api_edit(player_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    input_data = (content['fld_Name'], content['fld_Team'],
                  content['fld_Position'], content['fld_Age'],
                  content['fld_Height_inches'], content['fld_Weight_lbs'], player_id)
    sql_update_query = """UPDATE tblMlbPlayersImport t SET t.fld_Name = %s, t.fld_Team = %s, t.fld_Position = 
        %s, t.fld_Age = %s, t.fld_Height_inches = %s, t.fld_Weight_lbs = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, input_data)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


# Delete an existing Player by Id
@app.route('/api/v1/player/<int:player_id>', methods=['DELETE'])
def api_delete(player_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblMlbPlayersImport WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


# Jinga Template Views are below...
# Home Page - View all Players
@app.route('/', methods=['GET'])
def index():
    user = {'username': 'MLB Players Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMlbPlayersImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, players=result)


# View Player by Id
@app.route('/view/<int:player_id>', methods=['GET'])
def record_view(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMlbPlayersImport WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Player', player=result[0])


# Add New Player by Id Page
@app.route('/players/new', methods=['GET'])
@login_required
def form_insert_get():
    return render_template('new.html', title='New Player Form')


# Add New Player by Id Form
@app.route('/players/new', methods=['POST'])
@login_required
def form_insert_post():
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('fldPlayerName'), request.form.get('fldTeamName'),
                  request.form.get('fldPosition'), request.form.get('fldAge'),
                  request.form.get('fldHeight'), request.form.get('fldWeight'))
    sql_insert_query = """INSERT INTO tblMlbPlayersImport (fld_Name,fld_Team,fld_Position,fld_Age,fld_Height_inches,fld_Weight_lbs) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


# Edit Player by Id Page
@app.route('/edit/<int:player_id>', methods=['GET'])
@login_required
def form_edit_get(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblMlbPlayersImport WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', player=result[0])


# Edit Player by Id Form
@app.route('/edit/<int:player_id>', methods=['POST'])
@login_required
def form_update_post(player_id):
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('fldPlayerName'), request.form.get('fldTeamName'),
                  request.form.get('fldPosition'), request.form.get('fldAge'),
                  request.form.get('fldHeight'), request.form.get('fldWeight'), player_id)
    sql_update_query = """UPDATE tblMlbPlayersImport t SET t.fld_Name = %s, t.fld_Team = %s, t.fld_Position = 
    %s, t.fld_Age = %s, t.fld_Height_inches = %s, t.fld_Weight_lbs = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


# Delete Player by Id Form
@app.route('/delete/<int:player_id>', methods=['POST'])
@login_required
def form_delete_post(player_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblMlbPlayersImport WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
