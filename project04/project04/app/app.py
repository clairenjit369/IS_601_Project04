from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect, render_template, url_for, Blueprint, flash
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
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
                method='123456'
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
# View all Residents
@app.route('/api/v1/addresses', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


# View a single Resident record by Id
@app.route('/api/v1/addresses/<int:resident_id>', methods=['GET'])
def api_retrieve(resident_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses WHERE id=%s', resident_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


# Add a New Resident
@app.route('/api/v1/addresses', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    input_data = (content['fld_Name'], content['fld_Team'],
                  content['fld_Position'], content['fld_Age'],
                  content['fld_Height_inches'], content['fld_Weight_lbs'])
    sql_insert_query = """INSERT INTO addresses (Fname, Lname, Address, City, State, ZipCode) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, input_data)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


# Update an existing Resident by Id
@app.route('/api/v1/addresses/<int:resident_id>', methods=['PUT'])
def api_edit(resident_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    input_data = (content['fld_Name'], content['fld_Team'],
                  content['fld_Position'], content['fld_Age'],
                  content['fld_Height_inches'], content['fld_Weight_lbs'], resident_id)
    sql_update_query = """UPDATE addresses t SET t.Fname = %s, t.Lname = %s, t.Address = 
        %s, t.City = %s, t.State = %s, t.ZipCode = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, input_data)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


# Delete an existing Resident by Id
@app.route('/api/v1/addresses/<int:resident_id>', methods=['DELETE'])
def api_delete(resident_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM addresses WHERE id = %s """
    cursor.execute(sql_delete_query, resident_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


# Jinga Template Views are below...
# Home Page - View all Residents
@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Resident Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, residents=result)


# View Residents by Id
@app.route('/view/<int:resident_id>', methods=['GET'])
def record_view(resident_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses WHERE id=%s', resident_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Residents', residents=result[0])


# Add New Resident by Id Page
@app.route('/residents/new', methods=['GET'])
@login_required
def form_insert_get():
    return render_template('new.html', title='New Resident Form')


# Add New Resident by Id Form
@app.route('/residents/new', methods=['POST'])
@login_required
def form_insert_post():
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('Fname'), request.form.get('Lname'),
                  request.form.get('Address'), request.form.get('City'),
                  request.form.get('State'), request.form.get('ZipCode'))
    sql_insert_query = """INSERT INTO addresses (Fname, Lname, Address, City, State, ZipCode) VALUES (%s, %s,%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


# Edit Resident by Id Page
@app.route('/edit/<int:resident_id>', methods=['GET'])
@login_required
def form_edit_get(resident_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM addresses WHERE id=%s', resident_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', resident=result[0])


# Edit Resident by Id Form
@app.route('/edit/<int:resident_id>', methods=['POST'])
@login_required
def form_update_post(resident_id):
    cursor = mysql.get_db().cursor()
    input_data = (request.form.get('Fname'), request.form.get('Lname'),
                  request.form.get('Address'), request.form.get('City'),
                  request.form.get('State'), request.form.get('ZipCode'), resident_id)
    sql_update_query = """UPDATE addresses t SET t.Fname = %s, t.Lname = %s, t.Address = 
        %s, t.City = %s, t.State = %s, t.ZipCode = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, input_data)
    mysql.get_db().commit()
    return redirect("/", code=302)


# Delete Residents by Id Form
@app.route('/delete/<int:resident_id>', methods=['POST'])
@login_required
def form_delete_post(resident_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM addresses WHERE id = %s """
    cursor.execute(sql_delete_query, resident_id)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return render_template('login.jinja2')


@app.errorhandler(404)
def not_found(arg):
    """Page not found."""
    return render_template('404.html', title='404 error.', message='Page Not Found')


@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return render_template('400.html', title='400 error.', message='Bad request.  Page Not Found')


@app.errorhandler(500)
def server_error(arg):
    """Internal server error."""
    return render_template('500.html', message='Server Error')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
