from project2 import app
from project2 import connect
from project2 import queries
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import mysql.connector
import bcrypt

# set a secret key for the app
app.secret_key = b'_5#y2LF4Q8z\n\xec]/'

# Intialize MySQL


dbconn = None
connection = None
# #User global variable for passing logged in user information
employee = None
session = None

# connect to the database of employees and their hashed passwords
def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    port=connect.dbport, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def Login():
    # render the login page template
    return render_template("login.html",title="Login")

@app.route('/login', methods=['GET', 'POST'])
def login_post():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'employee_email' in request.form and 'password' in request.form:
        # Create variables for easy access
        employee_email = request.form['employee_email']
        password = request.form['password']
        # Check if account exists using MySQL
        connection=getCursor()
        connection.execute(queries.login)
        employee = connection.fetchone()
        connection.close()
        if employee:
            # If account exists in employee table in out database
            # Create session data, we can access this data in other routes
            session['employee_id'] = employee['employee_id']
            session['employee_email'] = employee['employee_email']
            session['employee_password'] = employee['employee_password']
            # Redirect to home page
            return redirect(url_for('dashboard'))
        else:
            # Account doesnt exist or username/password incorrect
            return render_template('login.html', error='Incorrect employee_email/password!')
    #get the form data from the request object
    employee_email = request.form['employee_email']
    password = request.form['password']
    #check if the employee exists in the database
    connection=getCursor()
    connection.execute(queries.login)
    employee = connection.fetchone()
    connection.close()
    if employee:
        #check if the password matches the stored hash
        if bcrypt.check_password_hash(employee['password'], password):
            #set the employee role type as a session variable
            session['employee_type'] = employee['role_name']
            #redirect to the dashboard page
            return redirect(url_for('dashboard'))
       
 #if the employee_email or password is incorrect, show an error message
    error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)
    
@app.route('/dashboard')
def dashboard():
    # Check if the employee is logged in and has an employee_type session variable set
    if 'employee_type' in session:
        # Render the dashboard template and pass the employee_type as a template variable
        return render_template('dashboard.html', employee_type=session['employee_type'])
    # If the employee is not logged in or has no employee_type set, redirect to the login page
    return redirect(url_for('login'))


