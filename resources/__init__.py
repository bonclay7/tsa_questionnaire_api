__author__ = 'grk'
from flask import Flask, make_response
from flask.ext import restful
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps
from flask_restful_swagger import swagger
import re


MONGO_URL = "mongodb://192.168.56.102:27017/ait"
SUPER_USER = "sioAdmin"

app = Flask(__name__)
#api = restful.Api(app)


def get_token(authorization):
    prog = re.compile('^(Bearer) (\w+)$')
    match = prog.match(authorization)
    if match:
        return match.group(2)
    else:
        return None


def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api = swagger.docs(restful.Api(app), apiVersion='0.1')


app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)