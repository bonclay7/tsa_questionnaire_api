from models.contact import Contact

__author__ = 'grk'
from flask.ext.restful import reqparse, fields
from validate_email import validate_email

def email(email_str):
    if validate_email(email_str):
        return email_str
    return None



class Publication:
    def __init__(self):
        self.by = None
        self.quiz = None
        self.to = None
        self.creationDate = None
        self.hash = ""
        self._id = ""

    @staticmethod
    def publication_from_dict(pubDict):
        p = Publication()
        p.by = pubDict.get('by')
        p.to = Contact.contact_from_dict(pubDict.get('to'))
        p.creationDate = pubDict.get('creationDate')
        p.hash = pubDict.get('hash')
        p._id = pubDict.get('_id')

        return p


    def format(self):
        return {
            "_id": self._id,
            "by": self.by,
            "to": self.to.format(),
            "creationDate": str(self.creationDate),
            "hash": self.hash,
            "quiz": self.quiz.format_http(),
        }

