__author__ = 'grk'
from flask import request, abort
from flask.ext.restful import Resource, reqparse, marshal_with
from resources import mongo, swagger, authorize, get_id, app
from models.quiz import creation_parser, Quiz, QuizStats, Question
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

    def post(self):
        session = authorize(request.headers["Authorization"])

        quiz_input = creation_parser.parse_args()
        quiz = Quiz.quiz_from_dict(quiz_input)
        quiz.creationDate = datetime.now()
        quiz.createdBy = session.get('user').get('login')

        """ we create the quiz first """
        quiz._id = int(get_id("quiz"))
        print "\n", quiz.format()
        mongo.db.quiz.insert(quiz.format())

        """ we create questions as objects and we embbed them into the quiz"""
        for qst in quiz.questions:
            self.add_question(qst, quiz)


        return {"quiz_id": "%s" % (quiz._id)}, 201

    def get(self, quiz_id=None):
        session = authorize(request.headers["Authorization"])

        if quiz_id is None:
            return self.get_all_quiz(session.get('user').get('login'))
        else:
            return (self.get_single_quiz(quiz_id)).format_http()

    def get_all_quiz(self, username):
        quiz = []
        results = mongo.db.quiz.find({"createdBy": username})

        for q in results:
            quiz.append(QuizStats.quiz_from_dict(q).format())

        return quiz

    def get_single_quiz(self, quiz_id):
        res = mongo.db.quiz.find_one_or_404({"_id": int(quiz_id)})
        quiz = Quiz.quiz_from_dict(res)
        return quiz

    def put(self, quiz_id):
        session = authorize(request.headers["Authorization"])
        user_login = session.get("user").get("login")

        """ we will parse the input first """


        quiz = self.get_single_quiz(quiz_id)


    def patch(self, quiz_id=None, question_id=None):
        print "popo"
        return "", 200