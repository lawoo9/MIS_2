from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)
app.secret_key = 'lawrence123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']='course123'
app.config['MYSQL_DB']='users'
mysql = MySQL(app)
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
   msg=''
if request.method == 'POST' and 'username' in request.form and 'password' in request
username=request.form['username']
password=request.form['password']
cursor=mysql.connection.cursor(mySQLdb.cursors.dictCursor)
cursor.execute('SELECT * FROM registrations WHERE username=%s AND user_pass=%s',(username, password))
account=cursor.fetchone()
if account:
   session['loggedin']=True
   session['id']=account['id']
   session['username']=account['username']
   msg='logged in successfully!'
   return render_template('index.html', msg=msg)
else:
   msg='Incorrect username/password!'   
   return render_template('login.html', msg=msg)
.route('/register', methods=['GET', 'POST'])
register():
msg=''
if request.method=='POST' and 'username' in request.form and 'password' in request.form:
username=request.form['username']
password=request.form['password']
cursor=mysql.connection.cursor(MySQLdb.cursors.Dictcursor)
cursor.execute('SELECT * FROM registrations WHERE username=%s', (username,))
account=cursor.fetchone()
if account:
   msg= 'Account already exist!'
elif not re.match(r'[A-Za-z0-9]+', username):
   msg='Username must contain only characters and numbers!'
elif not username or not password:
   msg='please fill out the form!'
else:
   cursor.execute('INSERT INTO registrations VALUES (NULL, %s, %s)'(username, password))
   mysql.connection.commit()
   msg='You have successfully registered!'
elif request.method=='POST':
msg='please fill out the form!'
return render_template('register.html', msg=msg)