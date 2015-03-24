from flask.ext.restful.utils.cors import crossdomain
from models.publication import Publication

__author__ = 'grk'
from flask.ext.restful import Resource, reqparse
from models.participation import Answer, Participation, participation_parser
from resources import mongo
from flask import request, abort
from resources import mongo, swagger, SUPER_USER, authorize, get_id


class ParticipationServices(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("Content-Type", type=str, location='headers', required=True,
                                 help="Content Type must be application/json")

    def get(self, pub_hash):
        return mongo.db.publications.find_one_or_404({"hash": pub_hash})


    def post(self, pub_hash):
        self.parser.add_argument("Authorization", type=str, location='headers', required=True,
                                 help="Authorization header missing")
        session = authorize(request.headers["Authorization"])
        print session
        print participation_parser.parse_args()