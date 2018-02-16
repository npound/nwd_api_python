#!/usr/bin/python

from flask import request, Flask
from flask_cors import CORS
from nwd_db import NWD_DB
from nwd_token import NWD_JWT
from nwd_sendgrid import NWD_SENDGRID
import json

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST', 'GET'])
def login():
    db = NWD_JWT()
    if request.method == 'POST':
        jo = request.json
        return '{"token":"'+ db.GetToken(jo['username'],jo['password']) +'"}'

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

@app.route('/SignUp', methods=['POST'])
def signup():
    db = NWD_DB()
    jo = request.json

    uid = db.create_new_user(jo['username'],jo['password'],jo['fname'],jo['lname'],jo['phone'])
    res =  str(uid != "")
    return '{"result":"'+res+'", "user_Id":"'+uid+'"}'

@app.route('/ResetPassword', methods=['POST', 'PUT'])
def reset_password():
    jo = request.json
    if request.method =='POST':
        sg = NWD_SENDGRID()
        sg.send_password_reset(jo['username'])
    elif request.method == 'PUT':
        db = NWD_DB()
        db.redeem_password_reset(jo['password'],jo['uuid'])
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return '{"result":True}'

@app.route('/VerifyToken', methods=['POST'])
def VerifyToken():
    jo = request.json
    db = NWD_JWT()
    return '{"result":'+db.VerifyToken(jo['token'])+'}'

@app.route('/AllUsers', methods=['GET'])
def get_all_users():
    db = NWD_DB()
    return json.dumps( {"users":db.get_all_users()})
