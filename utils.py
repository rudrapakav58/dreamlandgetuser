import json
import logging
import logging.handlers
import os
import sys
from functools import wraps
from flask import jsonify
from flask import abort, Blueprint, session, redirect, render_template, request, url_for
import constants as cts

__author__ = 'hughson.simon@gmail.com'

log_file = 'apps.log'

logging.basicConfig(level=logging.INFO, filename=log_file, format="%(asctime)s - %(name)s - %(message)s", datefmt="%H:%M:%S", filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        # Do something with your request here
        try:
            request.get_json()
        except Exception:
            #print e
            msg = "payload must be a valid json"
            return (jsonify({'response_status': cts.RESPONSE_ERROR,
                              'response_message': msg}), 400)
        return f(*args, **kw)
    return wrapper

def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json'])
    return best == 'application/json'

def is_json():
    """Validate if given input is json string"""
    try:
        json_object = json.loads(request.form)
    except ValueError:
        #print e
        return False
    return True, json_object

def  validate_registration_input(**data):
    """Validate if given input has mandatory keys"""
    MANDATORY_KEYS = ['email', "username", "name", "password"]
    if all(k in data.keys() for k in MANDATORY_KEYS):
        #if MANDATORY_KEYS in data.keys():# check mandatory keys
        return True, "SUCCESS"
    else:
        return False, ("Mandatory fields Not Provided")
