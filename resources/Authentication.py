from flask.ext.restful.utils.cors import crossdomain

__author__ = 'grk'

from flask.ext.restful import Resource
from flask import request
from models.user import User
from models.session import Session
from resources import authorize, swagger, mongo

import hashlib

class Authentication(Resource):



    def hash_password(self, password):
        return hashlib.sha256(password).hexdigest()



    @swagger.operation(notes='Get Api Token',
                       nickname='authenticate',
                       parameters=[
                           {
                                "name": "login",
                                "description": "user login",
                                "required": True,
                                "allowMultiple": False,
                                "dataType": str.__name__,
                                "paramType": "header"
                           },
                           {
                                "name": "password",
                                "description": "user password",
                                "required": True,
                                "allowMultiple": False,
                                "dataType": str.__name__,
                                "paramType": "header"
                           }
                       ]
    )
    @crossdomain(origin='*')
    def post(self):
        login = request.headers["X-Login"]
        password = request.headers["X-Password"]

        if (login or password) is None:
            return '', 404

        user_dict = mongo.db.users.find_one({"password": self.hash_password(password), "login": login})

        if user_dict is None:
            return '', 403

        session_dict = mongo.db.sessions.find_one({"user.login": login, "status": 0})

        """ we do not create a new session if already exists"""
        if session_dict is not None:
            return Session.session_from_dict(session_dict).format_http(), 201

        user_dict["_id"] = str(user_dict["_id"])
        user = User.user_from_dict(user_dict)

        session = Session.session_from_user(user)
        mongo.db.sessions.insert(session.format())

        return session.format_http(), 201


    @swagger.operation(notes='Release API Token',
                       nickname='disconnect',
                       parameters=[
                           {
                                "name": "token",
                                "description": "API Token",
                                "required": True,
                                "allowMultiple": False,
                                "dataType": str.__name__,
                                "paramType": "header"
                           }
                       ]
    )
    @crossdomain(origin='*')
    def delete(self):
        session_dict = authorize(request.headers["Authorization"])

        mongo.db.sessions.update({"token": session_dict.get('token'), "status": 0}, {"$set": {"status": 1}})

        print session_dict
        return '', 202