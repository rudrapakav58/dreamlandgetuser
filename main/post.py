from flask import abort, Blueprint, session, redirect, render_template, request, url_for
from flask_login import current_user
from flask_login import login_required
import psycopg2
import constants as cts
from utils import validate_json, validate_registration_input
from flask import jsonify
import datetime as dttim

__author__ = 'hughson.simon@gmail.com'

blueprint = Blueprint('herbs', __name__)

@blueprint.route("/post",methods=['GET', 'POST'])
@login_required
def post():

    try:
        result = request.form.to_dict()
        print(result)
        if result == {}:
            return render_template('dream_post.html')
        elif len(result['dream_type']) > 1:
            dream = result['dream']
            import random
            for x in range(1):
                id1 = random.randint(1, 100000)
            db = psycopg2.connect(
                database="dcore2hl3fm13v",
                user="pnevkxlqdlmdif",
                password="4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
                host="ec2-174-129-192-200.compute-1.amazonaws.com"
            )
            # db = psycopg2.connect(
            #     database="Dreamland",
            #     user="postgres",
            #     password="1234",
            #     host="localhost"
            # )
            cur = db.cursor()
            cur.execute(
                "INSERT INTO user_dreams (id,user_name,date_post,dream) VALUES ('{}',0,0,'{}')".format(
                    id1, result['dream']))
            # dreams_user=cur.execute("SELECT dream From user_dreams")
            print(id1)
            db.commit()
            print(result['dream'])
            db.close()
            db = psycopg2.connect(
                database="dcore2hl3fm13v",
                user="pnevkxlqdlmdif",
                password="4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
                host="ec2-174-129-192-200.compute-1.amazonaws.com"
            )
            # db = psycopg2.connect(
            #     database="Dreamland",
            #     user="postgres",
            #     password="1234",
            #     host="localhost"
            # )
            cur = db.cursor()
            cur.execute("SELECT dream From user_dreams")
            dream_user1 = cur.fetchall()
            # print(tuple())
            db.commit()
            db.close()
            dream_user = []
            for i in dream_user1:
                dream_user.append(str(i))
            post_type = result['category']
            msg = "Thanks for feeling  out your dream"
            return render_template('dream_post.html', dream=dream, msg=msg, dream_user=dream_user)
    except:
        pass
