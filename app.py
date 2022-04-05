from flask import Flask, render_template, request, session, jsonify, flash
from firebase import firebase
import pyrebase
import hashlib
import os
import time
import cv2
import numpy as np
import pandas as pd

def read_data(filename):
    data = pd.read_csv(filename)
    return data

review_data = read_data('res_data.csv')
user_data = read_data('user_message.csv')

app = Flask(__name__)
#configuration for firebase
CONFIG = {
"apiKey": "AIzaSyBmP0ROjOdlB8JdvDJJOdYDGcccSg3cF3I",
"authDomain": "food-review-f8f55.firebaseapp.com",
"databaseURL": "https://food-review-f8f55-default-rtdb.firebaseio.com",
"projectId": "food-review-f8f55",
"storageBucket": "food-review-f8f55.appspot.com",
"messagingSenderId": "763540278724",
"appId": "1:763540278724:web:5d7f88ae3f5bca8b53a891",
"measurementId": "G-JLS961T11B"
}


app.config.update(SECRET_KEY=os.urandom(100))
app.config['SESSION_TYPE'] = 'filesystem'
##------------------------------------------------------------------------------##
##__________________________utility functions______________________




def get_data(pro):
    global review_data
    hotels = []
    data_subset = review_data[review_data['Category'] == pro]
    for name in list(set(data_subset['Restaurant Name'])):
        hdict = {}
        hotel_subset = data_subset[data_subset['Restaurant Name'] == name]
        hdict['Restaurant Name'] = name
        hdict['Address'] = list(hotel_subset['Address'])[0]
        hdict['Rating text'] = list(hotel_subset['Rating text'])[0]
        hdict['image_name'] = os.path.join('res_images', name + '.png')
        # print(hdict['image_name'])
        hotels.append(hdict)
    return hotels


def get_data_single(res):
    global review_data
    hdict = {}
    hotel_subset = review_data[review_data['Restaurant Name'] == res]
    hdict['Restaurant Name'] = res
    hdict['Reviews'] = list(hotel_subset['Reviews'])
    hdict['User_email'] = list(hotel_subset['User_email'])
    hdict['Has Table booking'] = list(hotel_subset['Has Table booking'])[0]
    hdict['Average Cost for two'] = list(hotel_subset['Average Cost for two'])[0]
    hdict['Category'] = list(hotel_subset['Category'])[0]
    hdict['Address'] = list(hotel_subset['Address'])[0]
    hdict['Cuisines'] = list(hotel_subset['Cuisines'])[0]
    hdict['Has Online delivery'] = list(hotel_subset['Has Online delivery'])[0]
    hdict['Aggregate rating'] = list(hotel_subset['Aggregate rating'])[0]
    hdict['Rating text'] = list(hotel_subset['Rating text'])[0]
    hdict['Votes'] = list(hotel_subset['Votes'])[0]
    # hdict['image'] = cv2.imread(os.path.join('static','res_images', name + '.png'))
    hdict['image_name'] = os.path.join('res_images', res + '.png')
    return hdict



def logincheck(u_email, u_pass):
    fb_pyre = pyrebase.initialize_app(CONFIG)
    auth = fb_pyre.auth()
    try:
        signin = auth.sign_in_with_email_and_password(u_email, u_pass)
    except Exception as e:
        return False
    return True

def signupcheck(u_dict):
    fb = firebase.FirebaseApplication('https://food-review-f8f55-default-rtdb.firebaseio.com/')
    email = u_dict['email']
    res = hashlib.sha256(email.encode())
    sha_email = res.hexdigest()
    result = fb.get('/{}'.format(sha_email), None)
    if result != None:
        valid = False
        msg = 'Email already exists'
        return valid, msg
    else:
        valid = True
        msg = 'Succesfully created profile'
        return valid, msg

def update_db(user_dict):
    fb = firebase.FirebaseApplication('https://food-review-f8f55-default-rtdb.firebaseio.com//')
    fb_pyre = pyrebase.initialize_app(CONFIG)
    auth = fb_pyre.auth()
    email = user_dict['email']
    res = hashlib.sha256(email.encode())
    sha_email = res.hexdigest()
    result = fb.post('/{}'.format(sha_email), user_dict)
    flag = auth.create_user_with_email_and_password(email, user_dict['password'])
    if result != None and flag != None:
        status = True
        return status


##------------------------------------------------------------------------------##
##__________________pages_____________________________
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('index.html')

@app.route('/index_page')
def index_page():
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('index.html')




@app.route('/login_page')
def login_page():
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('login.html')

@app.route('/about')
def about_page():
    if 'username' in session:
        return render_template('about_loggedin.html', username = session['username'])
    else:
        return render_template('about.html')

@app.route('/contact')
def contact_page():
    if 'username' in session:
        return render_template('contact_loggedin.html', username = session['username'])
    else:
        return render_template('contact.html')



@app.route('/signup_page')
def accounts_page():
    if 'username' in session:
        return render_template('index_loggedin.html', username = session['username'])
    else:
        return render_template('signup.html')






##________________functional API________________________

@app.route("/bestofmumbai")
def review_MN():
    if 'username' in session:
        data = get_data(1)
        return render_template('bestofmumbai.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/alldaycafe")
def review_NC():
    if 'username' in session:
        data = get_data(2)
        return render_template('alldaycafe.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/kebabs")
def review_WI():
    if 'username' in session:
        data = get_data(3)
        return render_template('kebabs.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/oldisgold")
def review_CT():
    if 'username' in session:
        data = get_data(4)
        return render_template('oldisgold.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/corporate")
def review_VA():
    if 'username' in session:
        data = get_data(5)
        return render_template('corporate.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')

@app.route("/streetsavy")
def review_NY():
    if 'username' in session:
        data = get_data(6)
        return render_template('streetsavy.html', rows = data, username = session['username'])
    else:
        print('Please Login')
        return render_template('login.html')


@app.route("/show_info",methods=["POST"])
def show_info():
    if 'username' in session:
        res = request.form['res_name']
        print(res)
        data = get_data_single(res)
        return render_template('show_info.html', data = data, username = session['username'])
    else:
        return render_template('login.html')



@app.route("/logout")
def logout():
    if 'username' in session:
        session['logged_in'] = False
        session.pop('username')
    print(session)
    return render_template('index.html')




@app.route("/login", methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['pass']
    valid = logincheck(email, password)
    if valid:
        session['logged_in'] = True
        session['username'] = email
        print(session)
        return render_template('index_loggedin.html', username = session['username'])
    else:
        flash('Incorrect Username or Password')
        print('Incorrect Username or Password')
        return render_template('login.html')


@app.route("/comment", methods = ['POST'])
def comment():
    global review_data
    hdict = {}
    res = request.form['Restaurant Name']
    hdict['Reviews'] = request.form['Reviews']
    print(res)
    print(hdict['Reviews'])
    hotel_subset = review_data[review_data['Restaurant Name'] == res]
    hdict['Restaurant ID'] = list(hotel_subset['Restaurant ID'])[0]
    hdict['Restaurant Name'] = res
    hdict['Address'] = list(hotel_subset['Address'])[0]
    hdict['Cuisines'] = list(hotel_subset['Cuisines'])[0]
    hdict['Average Cost for two'] = list(hotel_subset['Average Cost for two'])[0]
    hdict['Has Table booking'] = list(hotel_subset['Has Table booking'])[0]
    hdict['Has Online delivery'] = list(hotel_subset['Has Online delivery'])[0]
    hdict['Aggregate rating'] = list(hotel_subset['Aggregate rating'])[0]
    hdict['Rating text'] = list(hotel_subset['Rating text'])[0]
    hdict['Votes'] = list(hotel_subset['Votes'])[0]
    hdict['Category'] = list(hotel_subset['Category'])[0]
    hdict['User_email'] = session['username']
    review_data = review_data.append(hdict, ignore_index = True)
    review_data.to_csv('res_data.csv', index = False)
    data = get_data_single(res)
    print(data)
    return render_template('show_info.html', data = data, username = session['username'])





@app.route("/signup", methods = ['POST'])
def signup():
    user = {}
    user['name'] = request.form['name']
    user['email'] = request.form['email']
    user['password'] = request.form['pass']
    valid, msg = signupcheck(user)
    print(valid, msg)
    if valid:
        status = update_db(user)
        if status:
            flash(msg)
            print(msg)
            return render_template('login.html')
        else:
            flash('Error in creating profile')
            print('Error in creating profile')
            return render_template('signup.html')
    else:
        flash(msg)
        print(msg)
        return render_template('signup.html')

@app.route("/contactmsg", methods = ['POST'])
def contact():
    global user_data
    user = {}
    user['Name'] = request.form['fname']
    user['Email'] = request.form['email']
    user['Phone'] = request.form['pno']
    user['Message'] = request.form['msg']
    print(user)
    user_data = user_data.append(user, ignore_index = True)
    user_data.to_csv('user_message.csv', index = False)
    return render_template('contact.html')



if __name__ == "__main__":
    app.secret_key = os.urandom(100)
    app.run(host='127.0.0.1', port=5000, debug = False )
