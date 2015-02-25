from flask.ext.restful.utils.cors import crossdomain

__author__ = 'grk'
from flask import request, abort
from flask.ext.restful import Resource, reqparse, fields, marshal_with
from resources import mongo, swagger, authorize, get_id
from models.quiz import creation_parser, Quiz, Question, AnswerTemplate
import hashlib
from datetime import datetime


class QuizResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("Content-Type", type=str, location='headers', required=True,
                                 help="Content Type must be application/json")
        self.parser.add_argument("Authorization", type=str, location='headers', required=True,
                                 help="Authorization header missing")



    def add_question(self, qst, quiz):
        qst._id = "%d.%d" % (quiz._id, qst.number)
        qst.creationDate = datetime.now()
        ans_dict = qst.answersTemplate
        qst.answersTemplate = []

        for ans in ans_dict:
            ans._id = "%s.%d" % (qst._id, ans.number)
            ans.creationDate = datetime.now()
            mongo.db.answersTemplate.insert(ans.format())
            qst.answersTemplate.append(ans.format())

        mongo.db.questions.insert(qst.format())
        mongo.db.quiz.update({"_id": quiz._id}, {"$push": {"questions": qst.format()}})



    @crossdomain(origin='*')
    def post(self):
        session = authorize(request.headers["Authorization"])

        quiz_input = creation_parser.parse_args()
        quiz = Quiz.quiz_from_dict(quiz_input)
        quiz.creationDate = datetime.now()
        quiz.createdBy = session.get('user').get('login')

        """ first we create the quiz """
        quiz._id = int(get_id("quiz"))
        mongo.db.quiz.insert(quiz.format())

        """ we create questions as objects and we embbed them into the quiz"""
        for qst in quiz.questions:
            self.add_question(qst, quiz)


        return "{'quiz_id':'%s'}" % (quiz._id), 201


    @crossdomain(origin='*')
    def get(self):
        id = get_id("popo")
        return "{'id':'%s'}" % (id), 201
