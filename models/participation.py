# -*- coding:utf-8 -*-
__author__ = 'grk'
from models.contact import Contact
from flask.ext.restful import reqparse, fields


participation_fields = {
    "quiz_id": fields.String,
    "pub_hash": fields.String,
    "pub_date": fields.String
}

participation_parser = reqparse.RequestParser()

participation_parser.add_argument('quiz_id', dest='quiz_id', type=str, location='json', required=True, help='quiz_id is missing', )
participation_parser.add_argument('pub_hash', dest='pub_hash', type=str, location='json', required=True, help='pub_hash is missing', )
participation_parser.add_argument('contact', dest='contact', type=str, location='json', required=False, )
participation_parser.add_argument('answers', dest='answers', type=list, location='json', required=False, )


class Answer:
    def __init__(self):
        self._id = None
        self.creationDate = None
        self.question = None
        self.value = None

    @staticmethod
    def answer_from_dict(answerDict):
        a = Answer()
        a._id = answerDict.get('_id')
        a.creationDate = answerDict.get('creationDate')
        a.value = answerDict.get('value')

        if not (answerDict.get('question') is None):
            a.question = Question.question_from_dict(answerDict.get('question'))

        return a

    def format(self):
        return {
            "_id": self._id,
            "value": self.value,
            "creationDate": str(self.creationDate),
            "question": self.question.format_http()
        }

    def format_http(self):
        return {
            "value": self.value,
            "creationDate": str(self.creationDate),
            "question": self.question.format_http()
        }


class Participation:
    def __init__(self):
        self.quiz_id = None
        self.pub_hash = None
        self.pub_date = None
        self.creationDate = None
        self.contact = None
        self.answers = []
        self._id = ""

    @staticmethod
    def participation_from_dict(pDict):
        p = Participation()
        p.quiz_id = pDict.get('quiz_id')
        p.pub_hash = pDict.get('pub_hash')
        p.pub_date = pDict.get('pub_date')
        p.creationDate = pDict.get('creationDate')
        p.contact = Contact.contact_from_dict(pDict.get('contact'))
        p._id = pDict.get('_id')

        if not (pDict.get('answers') is None):
            for a in pDict.get('answers'):
                p.answers.append(Answer.answer_from_dict(a))

        return p

    def format(self):

        formatted = {
            "_id": self._id,
            "quiz_id": self.by,
            "pub_hash": self.to.format(),
            "creationDate": str(self.creationDate),
            "pub_date": self.hash,
            "contact": self.contact.format(),
            "quiz": self.quiz.format_http(),
            "answers" : self.answers
        }

        """
        for a in self.answers:
            formatted["answers"].append(a.format_http())
        """

        return formatted
