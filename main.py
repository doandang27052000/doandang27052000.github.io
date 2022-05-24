from flask import Flask, render_template, redirect, url_for, request, session, jsonify, render_template_string, send_file,Response
from werkzeug.security import  generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flaskext.mysql import MySQL
import MySQLdb
import tablib
import codecs
import csv
from io import TextIOWrapper
import os
from models import model
import joblib
import traceback
import pickle
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import os
#from sklearn.model_selection import StratifiedKFold
#from sklearn.metrics import roc_auc_score

app = Flask(__name__, template_folder='templates', static_folder = 'static')

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Dang@0385721303'
app.config['MYSQL_DATABASE_DB'] = 'flaskdb'
from flaskext.mysql import MySQL
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
curs = conn.cursor()
print("connect to database successfully.")


@app.route('/')
def welcome():
    return redirect('/login.html')

@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/login.html', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        try: 
            errors = []
            _username = request.form.get('username', None)
            _password = request.form.get('password', None)
            sql0 = "SELECT pass FROM users WHERE username = '{0}'".format(_username)
            curs.execute(sql0)
            rows = curs.fetchone()
            if rows:
                dbPassword = rows[0]
                if check_password_hash(dbPassword, _password):
                    session['username'] = _username
                    return redirect(url_for('index'))

                else:
                    errors.append("Email/Password combination not found!")
                    return render_template('login.html', errors=errors)
        except Exception as e: 
            raise(e)
    else: 
        if 'username' in session:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')

@app.route('/logout', methods=['GET'])
def getLogout():
    session.pop('username')
    return render_template('login.html')

@app.route('/register.html', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        try: 
            errors = []
            _email = request.form.get('email', None)
            _name = request.form.get('name', None)
            _password = request.form.get('password', None)
            _username = request.form.get('username', None)
            _hassedpassword = generate_password_hash(_password)
            sql0 = "SELECT COUNT(*) FROM users WHERE email = '{0}'".format(_email)
            curs.execute(sql0)
            rows = curs.fetchone()
            if rows and rows[0] > 0:
                errors.append("Email already exists!")
                return render_template('register.html', errors = errors)
            elif _name and _email and _password: 
                sql1 = "INSERT INTO users(id, ten, username, email,pass) VALUES (null, '{0}', '{1}', '{2}', '{3}')".format( _name, _username,_email,_hassedpassword)
                curs.execute(sql1)
                conn.commit()
                return redirect(url_for('login'))
        except Exception as e: 
            raise(e)
    else: 
        if 'Email' in session:
            return redirect(url_for('index'))
        else:
            return render_template('register.html')


@app.route('/view_data.html', methods = ['GET', 'POST'])
def data():
    files = os.listdir("E:\\Study document\\Hệ hỗ trợ quyết định\\báo cáo\\Đang\\Project\\data")
    if request.method == "POST":
       data1 = request.form.get('comp_select')
       full_data = pd.read_csv('data/%s' %data1)
       return render_template('view_data.html', tables=[full_data.to_html(classes='data')], titles=full_data.columns.values, files = files)
    return render_template('view_data.html', files = files)

@app.route('/upload_data.html', methods=['GET','POST'])  
def uploadFile():
    files = os.listdir("E:\\Study document\\Hệ hỗ trợ quyết định\\báo cáo\\Đang\\Project\\data")
    if request.method == "POST":
        file = request.files['file']
        file.save(os.path.join('data', file.filename))
        return render_template('upload_data.html', message = "success")
    return render_template('upload_data.html')
@app.route('/detection.html', methods=['GET', 'POST'])
def detection():
    files = os.listdir("E:\\Study document\\Hệ hỗ trợ quyết định\\báo cáo\\Đang\\Project\\data")
    if request.method == "POST":
        data1 = request.form.get('comp_select')
        df = pd.read_csv('data/%s' % data1)
        predictions = model.pre_carinsurance(df)
        return render_template('detection.html', tables=[predictions.to_html(classes='data')], titles=predictions.columns.values, files = files)
    return render_template('detection.html', files = files)



if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(host='127.0.0.1', port=5003, debug=True)
   
