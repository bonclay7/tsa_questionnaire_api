from flask.ext.restful.utils.cors import crossdomain

__author__ = 'grk'
from flask import request, abort
from flask.ext.restful import Resource, reqparse, fields, marshal_with
from resources import mongo, swagger, SUPER_USER, authorize, get_id
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
    @crossdomain(origin='*')
    @marshal_with(user_fields)
    def post(self):
        authorize(request.headers["Authorization"])

        user = User.user_from_dict(post_parser.parse_args())
        user.password = hashlib.sha256(user.password).hexdigest()
        user.creationDate = datetime.now()

        existing = mongo.db.users.find_one({"login":user.login})

        if not (existing is None):
            abort(409)

        user_id = mongo.db.users.insert(user.format_for_create())
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
    @crossdomain(origin='*')
    def get(self, login=None):
        authorize(request.headers["Authorization"])

        if login is None:
            return self.get_all_users()
        else:
            return self.get_a_user(login)



    def get_all_users(self):
        users = []
        for user in mongo.db.users.find():
            users.append(User.user_from_dict(user).format())

        return users, 200

    def get_a_user(self, login):
        user = mongo.db.users.find_one_or_404({"login": login})
        return User.user_from_dict(user).format(), 200

    @swagger.operation(notes='Modify a user',
                       nickname='modify user',
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
    @crossdomain(origin='*')
    @marshal_with(user_fields)
    def put(self, login):
        authorize(request.headers["Authorization"])

        if login == SUPER_USER:
            abort(403)

        existing = mongo.db.users.find_one({"login": login})
        if existing is None:
            abort(404)

        user_edit = User.user_from_dict(post_parser.parse_args())
        user_edit.password = hashlib.sha256(user_edit.password).hexdigest()
        user_edit.creationDate = existing.get('creationDate')

        print user_edit.format()

        mongo.db.users.update({"login": login}, {"$set": user_edit.format_for_update()})

        print "modified : ", user_edit

        return user_edit, 201



    @swagger.operation(notes='Delete a user',
                       nickname='delete a user',
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
    @crossdomain(origin='*')
    def delete(self, login):
        authorize(request.headers["Authorization"])

        if login == SUPER_USER:
            abort(403)

        existing = mongo.db.users.find_one({"login": login})
        if existing is None:
            abort(404)

        user_delete = User.user_from_dict(existing)
        user_delete.deleteDate = datetime.now()

        delete_id = mongo.db.users_deleted.insert(user_delete.format_for_delete())

        mongo.db.users.remove({"login": login})

        print "deleted : ", delete_id

        return {"message": "deleted"}, 200


