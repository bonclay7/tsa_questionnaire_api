# -*- coding:utf-8 -*-
__author__ = 'grk'
from flask import request, abort
from flask.ext.restful import Resource, reqparse
from resources import mongo, authorize, get_id
from models.quiz import creation_parser, Quiz, QuizStats, patch_parser, put_parser
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

    """ here we will just add one or many questions to a quiz as an array"""
    def put(self, quiz_id):
        session = authorize(request.headers["Authorization"])
        put_request = Quiz.quiz_from_dict(put_parser.parse_args())

        criteria = {"createdBy": session.get('user').get('login'), "_id": int(quiz_id)}
        quiz = Quiz.quiz_from_dict(mongo.db.quiz.find_one_or_404(criteria))

        for qst in put_request.questions:
            self.add_question(qst, quiz)

        return {"message": "modified % s" % quiz_id}, 200

    """ modify some elements about the quiz, not the questions"""
    def patch(self, quiz_id):
        session = authorize(request.headers["Authorization"])
        patch_request = Quiz.quiz_from_dict(patch_parser.parse_args()).format_patch()

        if len(patch_request) == 0:
            abort(400)

        criteria = {"createdBy": session.get('user').get('login'), "_id": int(quiz_id)}
        mongo.db.quiz.find_one_or_404(criteria)
        mongo.db.quiz.update(criteria, {"$set": patch_request})

        return {"message": "modified % s" % quiz_id}, 200

    def delete(self, quiz_id, question_id=None):
        session = authorize(request.headers["Authorization"])

        if question_id is None:
            return self.delete_quiz(session.get('user').get('login'), quiz_id)
        else:
            return self.delete_question(session.get('user').get('login'), quiz_id, question_id)

    def delete_quiz(self, login, quiz_id):
        criteria = {"createdBy": login, "_id": int(quiz_id)}
        delete = mongo.db.quiz.find_one_or_404(criteria)
        mongo.db.quiz_deleted.insert(delete)

        #TODO : Supression des questions associées

        mongo.db.quiz_deleted.update(criteria, {"$set": {"deleteDate": str(datetime.now())}})
        mongo.db.quiz.remove(criteria)

        return None, 204

    def delete_question(self, login, quiz_id, question_id):
        criteria = {"createdBy": login, "_id": int(quiz_id), "questions._id": "%s.%s" % (quiz_id, question_id)}
        question_criteria = {"_id": "%s.%s" % (quiz_id, question_id)}
        """ we check in the db if the question is there and we rise and 404 response otherwise """
        mongo.db.quiz.find_one_or_404(criteria)

        """ we delete the question in the db system """
        mongo.db.questions.remove(question_criteria)

        """ we remove it from the quiz array """
        mongo.db.quiz.update(criteria, {"$pull": {"questions": question_criteria}})

        return None, 204
