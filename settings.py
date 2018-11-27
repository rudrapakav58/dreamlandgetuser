from datetime import timedelta
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
BCRYPT_LOG_ROUNDS = 13

ASSETS_DEBUG = False
DEBUG_TB_ENABLED = False  # Disable Debug toolbar
DEBUG_TB_INTERCEPT_REDIRECTS = False
LOG_RESPONSE = True

CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
WTF_CSRF_ENABLED = False

SQLALCHEMY_COMMIT_ON_TEARDOWN = True


ADMINS = ['sridhar@gmail.com', 'hughson.simon@gmail.com']
MANAGERS = ADMINS

#SERVER_NAME = 'http://127.0.0.1:5000/'

DEBUG = False
TESTING = False
DB = {
    'host': 'localhost:5432',
    'user': 'postgres',
    'password': '',
    'database': 'rateit',
}

PERMANENT_SESSION_LIFETIME = timedelta(minutes=25)
SECRET_KEY = '\xcb\xe2\xaf%\xaeV(\xf9S\xa1\xa1\x90\xf5\xfd>\xdey\x18\x8f04\xfa\xed\x84'

MAIL_SERVER = 'mail.smtp2go.com'
MAIL_PORT = 2525  # 8025, 587 and 25 can also be used.
MAIL_USE_TSL = True
MAIL_USERNAME = 'hughson.simon@gmail.com'
MAIL_PASSWORD = 'N2L1A6lSAZEp'
MAIL_DEFAULT_SENDER = 'support@rateit.com'

STRIPE_PUBLIC_KEY = 'pk_live_45ReJuOvb13kbGNZKOWH387Q'
STRIPE_SECRET_KEY = 'sk_live_pGUCOxgW15L6xqlv7ezeKcZH'


INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles"
)
