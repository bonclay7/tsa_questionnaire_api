from flask.ext.restful.utils.cors import crossdomain
from models.publication import Publication

__author__ = 'grk'
from flask import request, abort
from flask.ext.restful import Resource, reqparse, fields, marshal_with
from resources import mongo, swagger, SUPER_USER, authorize, get_id
from models.quiz import creation_parser, Quiz, QuizStats, patch_parser, put_parser
from models.user import User, post_parser, user_fields
from models.contact import Contact
import hashlib
from datetime import datetime
import smtplib
from email.mime.text import MIMEText


class ParticipationServices(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("Content-Type", type=str, location='headers', required=True,
                                 help="Content Type must be application/json")

    def get(self, pub_hash):
        return mongo.db.publications.find_one_or_404({"hash": pub_hash})


    def post(self, pub_hash):
        pass