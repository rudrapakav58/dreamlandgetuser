#!flask/bin/python
import sys
from flask import Flask
import extensions
from main import views,post
import utils as utl
from flask import jsonify
from flask_cors import CORS
import emails
# @TODO: add this as a command line tool
debug_config = False

def register_blueprints(app):
    app.register_blueprint(views.blueprint)
    app.register_blueprint(post.blueprint)
    return None


def create_app(config_object="prod"):
    app = Flask(__name__)
    app.config.from_object('config_debug' if debug_config else 'config')
    extensions.db.init_app(app)
    emails.mail.init_app(app)
    extensions.login_manager.init_app(app)
    extensions.login_manager.session_protection = 'strong'
    extensions.login_manager.login_view = "/login"
    register_blueprints(app)
    return app


app = create_app("prod")
CORS(app)


@app.errorhandler(403)
def error_403(e):
    return (jsonify({'response_status': "ERROR"},
                    {'response_message': "Coming Soon"}), 200)


@app.errorhandler(404)
def error_404(e):
    return (jsonify({'response_status': "ERROR",
                     'response_message': "Coming Soon"}), 200)


@app.errorhandler(405)
def error_405(e):
    return (jsonify({'response_status': "ERROR",
                     'response_message': "METHOD NOT ALLOWED"}), 200)


@app.errorhandler(500)
def error_500(e):
    return (jsonify({'response_status': "ERROR",
                     'response_message': "Internal Server Error"}), 200)
if __name__ == '__main__':
    logger = utl.logging
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', debug=True, port=port)