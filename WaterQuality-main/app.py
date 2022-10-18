import pickle
from flask import Flask, render_template, request
import numpy as np
import os
from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql 
import re 

app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'

mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'testingdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/index', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        # request all the input fields
        ph = float(request.form['ph value'])
        Hardness = float(request.form['Hardness'])
        Solids = float(request.form['Solids'])
        Chloramines = float(request.form['Chloramines'])
        Sulfate = float(request.form['Sulfate'])
        Conductivity = float(request.form['Conductivity'])
        Organic_carbon = float(request.form['Organic carbon'])
        Trihalomethanes = float(request.form['Trihalomethanes'])
        Turbidity = float(request.form['Turbidity'])

        # create numpy array for all the inputs
        val = np.array([ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity])

        # define save model and scaler path
        model_path = os.path.join('models', 'xgboost.sav')
        scaler_path = os.path.join('models', 'scaler.sav')

        # load the model and scaler
        model = pickle.load(open(model_path, 'rb'))
        scc = pickle.load(open(scaler_path, 'rb'))

        # transform the input data using pre fitted standard scaler
        data = scc.transform([val])

        # make a prediction for the given data
        res = model.predict(data)

        if res == 1:
            outcome = 'Potable'
        else:
            outcome = 'not potable'
        return render_template('index.html', result=outcome)
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def login():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM account WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
   
    # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    
    return render_template('login.html', msg=msg)
 
# http://localhost:5000/register - this will be the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
 # connect
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
   
  #Check if account exists using MySQL
        cursor.execute('SELECT * FROM account WHERE username = %s', (username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO account VALUES (NULL, %s, %s, %s, %s)', (fullname, username, password, email)) 
            conn.commit()
   
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
  
# run application
if __name__ == "__main__":
    app.run(debug=True)
