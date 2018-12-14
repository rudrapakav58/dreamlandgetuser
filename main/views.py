"""Purpose is to server general requests of the app"""

import json
from flask import render_template, jsonify, make_response,redirect,request
from flask import Blueprint
#from models import models
import psycopg2
import base64
from flask_login import current_user
from flask_login import login_user, logout_user, login_required
from flask import session as flask_sess
#from forms import LoginForm, RegistrationForm
import smtplib
from email.mime.text import MIMEText
import random
import string
blueprint = Blueprint('views', __name__)
def jsoner(file, status=None, result=None):
    mkres = render_template(file, status=status, result=json.dumps(result))
    response = make_response(mkres)
    response.headers['content-type'] = 'application/json'
    return response
@blueprint.route('/')
@login_required
def index():
    # try:
    #     result = request.form.to_dict()
    #     # print(result)
    #
    # except:
    #     pass
    # try:
    #     if result == {}:
    return render_template('dream_post.html')
    # except:
    #     pass
    # try:
    #     mail_id = result['mail']
    #     db = psycopg2.connect(
    #         database="dcore2hl3fm13v",
    #         user="pnevkxlqdlmdif",
    #         password="4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
    #         host="ec2-174-129-192-200.compute-1.amazonaws.com"
    #     )
    #     # print(db)
    #     # db = psycopg2.connect(
    #     #     database="Dreamland",
    #     #     user="postgres",
    #     #     password="1234",
    #     #     host="localhost"
    #     # )
    #     cur = db.cursor()
    #     cur.execute("SELECT email FROM test_user1 where email='{}'".format(mail_id))
    #     email_id = cur.fetchone()
    #     db.commit()
    #     # print(" user info created successfully")
    #     db.close()
    #     db_mailid = str(email_id)
    #     # print(type(db_mailid))
    #     # print(type(mail_id))
    #     if email_id == None:
    #         try:
    #             # print(type(mail_id))
    #             if result['password'] != result['c_password']:
    #                 # print(type(mail_id))
    #                 msg = "Passwords do not match"
    #                 return render_template('reg_user.html', msg=msg)
    #             elif result['password'] == result['c_password']:
    #                 # print(type(mail_id))
    #                 print(result['first_name'])
    #                 db = psycopg2.connect(
    #                     database="dcore2hl3fm13v",
    #                     user="pnevkxlqdlmdif",
    #                     password="4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
    #                     host="ec2-174-129-192-200.compute-1.amazonaws.com"
    #                 )
    #                 # db = psycopg2.connect(
    #                 #     database="Dreamland",
    #                 #     user="postgres",
    #                 #     password="1234",
    #                 #     host="localhost"
    #                 # )
    #                 enc = base64.b64encode(result['password'].encode())
    #                 enc = enc.decode()
    #                 cur = db.cursor()
    #                 cur.execute(
    #                     "INSERT INTO test_user1 (First_name,Last_name,Email,Password,Dob,Gender) VALUES ('{}','{}','{}','{}',0,0)".format(
    #                         result['first_name'], result['last_name'], result['mail'], enc))
    #                 db.commit()
    #                 # print(" user info created successfully")
    #                 db.close()
    #                 msg = "You Are Now A Registered User!"
    #                 # return render_template('reg_user.html',msg=msg)
    #                 return redirect('/post')
    #         except:
    #             pass
    #     else:
    #         # print(db_mailid)
    #         # print(mail_id)
    #         msg = "The email address you have entered is already registered!"
    #         # print(msg)
    #         return render_template('reg_user.html', msg=msg)
    #
    # except:
    #     pass


@blueprint.route('/register', methods=['GET', 'POST'])
def adminRegister():
    #form=RegistrationForm(request.form)

    if request.method == "POST":
        result = request.form.to_dict()
        print(result)
        try:
            mail_id=result['mail']
            db = psycopg2.connect(
                database="d5c3kekvf7cuup",
                user="gpthqvlaxsrwoq",
                password="9e12360d9c5c3faef58af66954d23af49d19991549fdd787969b9a80aa8e9c70",
                host="ec2-54-235-156-60.compute-1.amazonaws.com"
            )
            print(db)
            # db = psycopg2.connect(
            #     database="Dreamland",
            #     user="postgres",
            #     password="1234",
            #     host="localhost"
            # )
            cur = db.cursor()
            cur.execute("SELECT Email FROM test_user where Email='{}'".format(mail_id))
            email_id = cur.fetchone()
            db.commit()
            print(" user info created successfully")
            db.close()
            db_mailid=str(email_id)
            # print(type(db_mailid))
            # print(type(mail_id))
            if email_id==None:
                try:
                    # print(type(mail_id))
                    if result['password'] != result['c_password']:
                        # print(type(mail_id))
                        msg="Passwords do not match"
                        return render_template('reg_user.html',msg=msg)
                    elif result['password'] == result['c_password']:
                        # print(type(mail_id))
                        # print(result['first_name'])
                        db = psycopg2.connect(
                            database="d5c3kekvf7cuup",
                            user="gpthqvlaxsrwoq",
                            password="9e12360d9c5c3faef58af66954d23af49d19991549fdd787969b9a80aa8e9c70",
                            host="ec2-54-235-156-60.compute-1.amazonaws.com"
                        )
                        # db = psycopg2.connect(
                        #     database="Dreamland",
                        #     user="postgres",
                        #     password="1234",
                        #     host="localhost"
                        # )
                        enc = base64.b64encode(result['password'].encode())
                        enc = enc.decode()
                        cur = db.cursor()
                        cur.execute(
                            "INSERT INTO test_user (First_name,Last_name,Email,Password) VALUES ('{}','{}','{}','{}')".format(
                                result['first_name'], result['last_name'], result['mail'], enc))
                        db.commit()
                        #print(" user info created successfully")
                        db.close()
                        msg="You Are Now A Registered User!"
                        #return render_template('register.html',msg=msg)
                        return redirect('/post')
                except:
                    pass
            else:
                # print(db_mailid)
                # print(mail_id)
                msg = "The email address you have entered is already registered!"
                #print(msg)
                return render_template('reg_user.html', msg=msg)
        except:
            pass
    else:
        return redirect('/login')
@blueprint.route('/login', methods=['GET', 'POST'])
def Login():
    error = None
    #login_form = LoginForm(csrf_enabled=True)
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['password']
        print(password)
        db = psycopg2.connect(
            database="d5c3kekvf7cuup",
            user="gpthqvlaxsrwoq",
            password="9e12360d9c5c3faef58af66954d23af49d19991549fdd787969b9a80aa8e9c70",
            host="ec2-54-235-156-60.compute-1.amazonaws.com"
        )
        # db = psycopg2.connect(
        #     database="Dreamland",
        #     user="postgres",
        #     password="1234",
        #     host="localhost"
        # )
        cur = db.cursor()
        cur.execute("SELECT Email,Password FROM test_user where Email='{}'".format(email))
        mail_user = cur.fetchone()
        print(mail_user)
        if mail_user == None:
            msg = "Username is incorrect."
            return render_template('login.html', msg=msg)
        elif str(email) == mail_user[0]:
            cur.execute("SELECT Password From test_user where Email='{}'".format(email))
            password_user = cur.fetchone()
            print(password_user)
            enc_pass = base64.b64decode(password_user[0].encode())
            user_password=enc_pass.decode("utf-8")
            if user_password == password:
                msg = "You are logged in"
                #return render_template('login.html', msg=msg)
                # if 'remember_me' in request.form:
                #     remember_me = True
                # if mail_user.password_user:
                #     flask_sess['user_id'] = mail_user.userId
                #     login_user(mail_user, remember=remember_me)
                return redirect("/post")
            else:
                msg = "Password is incorrect."
                return render_template('login.html', msg=msg)
    else:
        user = current_user
        logout_user()
        flask_sess.clear()
        logout_user()
    return render_template('index.html')
@blueprint.route('/logout',methods=['GET', 'POST'])
def logout():
    """Logout the current user."""
    try:
        user = current_user
        user.authenticated = False
        logout_user()
        flask_sess.clear()
        logout_user()
    except Exception as e:
        print(e)
        # return e
    return redirect("/login")