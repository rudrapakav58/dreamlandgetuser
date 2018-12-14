from flask import abort, Blueprint, session, redirect, render_template, request, url_for
import psycopg2
blueprint = Blueprint('post', __name__)
@blueprint.route("/post",methods=['GET', 'POST'])
# @login_required
def post():
    try:
        result = request.form.to_dict()
        print(result)
        if result == {}:
            # db = psycopg2.connect(
            #     database="Dreamland",
            #     user="postgres",
            #     password="1234",
            #     host="localhost"
            # )
            # cur = db.cursor()
            # cur.execute("SELECT dream From user_dreams1")
            # dream_user1 = reversed(cur.fetchall())
            # # print(tuple())
            # db.commit()
            # db.close()
            # dream_user = []
            # for i in dream_user1:
            #     #j=reversed(str(i))
            #     dream_user.append(str(i))
            # post_type = result['category']
            # msg = "Thanks for feeling  out your dream"
            db = psycopg2.connect(
                database="d5c3kekvf7cuup",
                user="gpthqvlaxsrwoq",
                password="9e12360d9c5c3faef58af66954d23af49d19991549fdd787969b9a80aa8e9c70",
                host="ec2-54-235-156-60.compute-1.amazonaws.com"
            )
            cur = db.cursor()
            cur.execute("SELECT dream From user_dreams1")
            dream_user1 = reversed(cur.fetchall())
            # print(tuple())
            db.commit()
            db.close()
            dream_user = []
            for i in dream_user1:
                # j=reversed(str(i))
                dream_user.append(str(i))
            msg = "Thanks for feeling  out your dream"
            return render_template('dream_post.html',msg=msg, dream_user=dream_user)
        elif len(result['dream_type']) > 1:
            dream = result['dream']
            import random
            for x in range(1):
                id1 = random.randint(1, 100000)
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
            cur.execute(
                "INSERT INTO user_dreams1 (id,user_name,date_post,dream) VALUES ('{}',0,0,'{}')".format(
                    id1, result['dream']))
            # dreams_user=cur.execute("SELECT dream From user_dreams")
            print(id1)
            db.commit()
            print(result['dream'])
            db.close()
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
            cur.execute("SELECT dream From user_dreams1")
            dream_user1 = reversed(cur.fetchall())
            # print(tuple())
            db.commit()
            db.close()
            dream_user = []
            for i in dream_user1:
                #j=reversed(str(i))
                dream_user.append(str(i))
            post_type = result['category']
            msg = "Thanks for feeling  out your dream"
            return render_template('dream_post.html', dream=dream, msg=msg, dream_user=dream_user)
    except:
        pass
@blueprint.route("/profile",methods=['GET', 'POST'])
# @login_required
def update():
    print("hello")
    result = request.form.to_dict()
    print(len(result))
    return render_template('profile.html')
@blueprint.route("/delete", methods=['GET', 'POST'])
# @login_required
def delete():
    result = request.form.to_dict()
    print(result)
    try:
        if len(result)>0:
            return "Hey! Your post has been deleted"
        else:
            return {'response_status': "ERROR",'response_message': "Coming Soon"}
    except:
        pass
@blueprint.route("/tag", methods=['GET', 'POST'])
# @login_required
def tag():
    result = request.form.to_dict()
    print(result)
    try:
        if len(result) > 0:
            return render_template('tag.html')
        else:
            return {'response_status': "ERROR", 'response_message': "Coming Soon"}
    except:
        pass