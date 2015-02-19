__author__ = 'grk'

from flask.ext.restful import Resource
from resources import mongo
from resources import swagger

class HelloWorld(Resource):

    @swagger.operation(notes='dhgehgde')
    def get(self):
        return mongo.db.users.find()
