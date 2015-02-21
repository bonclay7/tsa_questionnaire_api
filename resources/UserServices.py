__author__ = 'grk'
from flask.ext.restful import Resource, reqparse, fields, marshal_with
from resources import mongo
from resources import swagger
from flask import request
from flask import abort
from resources import get_token
from models.user import User, post_parser, user_fields
import hashlib
from datetime import datetime

class UserServices(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("Content-Type", type=str, location='headers', required=True,
                                 help="Content Type must be application/json")
        self.parser.add_argument("Authorization", type=str, location='headers', required=True,
                                 help="Authorization header missing")


    @swagger.operation(notes='Create a user',
                       nickname='create user',
                       parameters=[
                           {
                               "name": "Authorization",
                               "description": "API Token (Bearer api_token)",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": str.__name__,
                               "paramType": "header"
                           },
                           {
                               "name": "user",
                               "description": "User json",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": str.__name__,
                               "paramType": "body"
                           }
                       ]
    )
    @marshal_with(user_fields)
    def post(self):
        token = get_token(request.headers["Authorization"])

        if token is None:
            abort(403)

        session_dict = mongo.db.sessions.find_one({"token": token, "status": 0})

        if session_dict is None:
            abort(403)

        user = User.user_from_dict(post_parser.parse_args())
        user.password = hashlib.sha256(user.password).hexdigest()
        user.creationDate = datetime.now()

        user_id = mongo.db.users.insert(user.format())
        user._id = user_id
        print "inserted : ", user_id

        return user, 201


    @swagger.operation(notes='Get a user',
                       nickname='get a user',
                       parameters=[
                           {
                               "name": "Authorization",
                               "description": "API Token (Bearer api_token)",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": str.__name__,
                               "paramType": "header"
                           },
                           {
                               "name": "login",
                               "description": "User login",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": str.__name__,
                               "paramType": "path"
                           }
                       ]
    )
    def get(self, login):
        token = get_token(request.headers["Authorization"])

        if token is None:
            abort(403)

        session_dict = mongo.db.sessions.find_one({"token": token, "status": 0})

        if session_dict is None:
            abort(403)

        user = mongo.db.users.find_one_or_404({"login": login})

        return User.user_from_dict(user).format(), 200


class UserListServices(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("Content-Type", type=str, location='headers', required=True,
                                 help="Content Type must be application/json")
        self.parser.add_argument("Authorization", type=str, location='headers', required=True,
                                 help="Authorization header missing")



    @swagger.operation(notes='Get all users',
                       nickname='get all users',
                       parameters=[
                           {
                               "name": "Authorization",
                               "description": "API Token (Bearer api_token)",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": str.__name__,
                               "paramType": "header"
                           }
                       ]
    )
    def get(self):
        token = get_token(request.headers["Authorization"])

        if token is None:
            abort(403)

        session_dict = mongo.db.sessions.find_one({"token": token, "status": 0})

        if session_dict is None:
            abort(403)

        users = []

        for user in mongo.db.users.find():
            users.append(User.user_from_dict(user).format())

        print(users)

        return users, 200



