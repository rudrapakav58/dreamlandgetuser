import sys
from flask import Flask, render_template, session
from flask import jsonify, g, url_for
import emails
import settings
import views
import extensions
from database import db_session

__author__ = 'hughson.simon@gmail.com'

app = Flask(__name__)

def create_app(config_object="prod"):
    app = Flask(__name__)
    app.config.from_object(settings)
    extensions.db.init_app(app)
    extensions.login_manager.init_app(app)
    extensions.login_manager.session_protection = 'strong'
    emails.mail.init_app(app)
    register_blueprints(app)
    wrap_teardown_funcs(app)
    register_errorhandlers(app)
    return app

def register_blueprints(app):
    app.register_blueprint(views.rate_index.blueprint)
    #app.register_blueprint(admin.admin.blueprint)
    return None

def wrap_teardown_funcs(app):
    def wrap_teardown_func(teardown_func):
        def log_teardown_error(*args, **kwargs):
            try:
                teardown_func(*args, **kwargs)
            except Exception as exc:
                app.logger.exception(exc)

        return log_teardown_error

    if app.teardown_request_funcs:
        for bp, func_list in app.teardown_request_funcs.items():
            for i, func in enumerate(func_list):
                app.teardown_request_funcs[bp][i] = wrap_teardown_func(func)
    if app.teardown_appcontext_funcs:
        for i, func in enumerate(app.teardown_appcontext_funcs):
            app.teardown_appcontext_funcs[i] = wrap_teardown_func(func)


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        emails.error_email()
        if error_code in [401, 404, 500]:
            return render_template("{0}.html".format(403)), 403
        else:
            return render_template("{0}.html".format(error_code)), error_code

    # for errcode in [401, 404, 500]:
    app.errorhandler(401)(render_error)
    return None

@app.before_request
def before_request(response):
    print "&" * 40


@app.after_request
def after_request(response):
    print "&" * 40

app = create_app("prod")

@app.errorhandler(403)
def error_403(e):
    return (jsonify({'status': "Error"}, {'Message': "Not Authorized"}), 403)


@app.errorhandler(404)
def error_404(e):
    return (jsonify({'response_status': "ERROR",
                     'response_message': "Not Authorized"}), 404)

@app.errorhandler(405)
def error_405(e):
    return (jsonify({'response_status': "ERROR",
                     'response_message': "METHOD NOT ALLOWED"}), 405)

@app.errorhandler(500)
def error_500(e):
    return (jsonify({'response_status': "ERROR",
                     'response_message': "Internal Server Error"}), 500)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    port = None
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    app.run(host='0.0.0.0', debug=True, port=port)
