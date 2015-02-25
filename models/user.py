__author__ = 'grk'
from flask.ext.restful import reqparse, fields
from validate_email import validate_email

def email(email_str):
    if validate_email(email_str):
        return email_str
    return None



user_fields = {
    'login': fields.String,
    'email': fields.String,
    'firstname': fields.String,
    'lastname': fields.String,
    'creationDate': fields.DateTime
}

post_parser = reqparse.RequestParser()
post_parser.add_argument('login', dest='login', type=str, location='json', required=True, help='login is missing', )
post_parser.add_argument('password', dest='password', type=str, location='json', required=True,
                         help='password is missing', )
post_parser.add_argument('firstname', dest='firstname', type=str, location='json', required=True,
                         help='firstname is missing', )
post_parser.add_argument('lastname', dest='lastname', type=str, location='json', required=True,
                         help='lastname is missing', )
post_parser.add_argument('email', dest='email', type=email, location='json', required=True, help='The user\'s email', )


class User:
    def __init__(self):
        self.login = ""
        self.password = ""
        self.email = ""
        self.creationDate = ""
        self.firstname = ""
        self.lastname = ""
        self.deleteDate = ""
        self._id = ""

    @staticmethod
    def user_from_dict(userDict):
        u = User()
        u.login = userDict.get('login')
        u.password = userDict.get('password')
        u.email = userDict.get('email')
        u.creationDate = userDict.get('creationDate')
        u.firstname = userDict.get('firstname')
        u.lastname = userDict.get('lastname')
        u._id = userDict.get('_id')
        return u


    def format(self):
        return {
            "login": self.login,
            "email": self.email,
            "creationDate": str(self.creationDate),
            "firstname": self.firstname,
            "lastname": self.lastname
        }

    def format_for_update(self):
        return {
            "email": self.email,
            "password": self.password,
            "firstname": self.firstname,
            "lastname": self.lastname
        }

    def format_for_delete(self):
        return {
            "login": self.login,
            "email": self.email,
            "creationDate": str(self.creationDate),
            "deleteDate": str(self.deleteDate),
            "firstname": self.firstname,
            "lastname": self.lastname
        }

    def format_for_create(self):
        return {
            "login": self.login,
            "email": self.email,
            "creationDate": str(self.creationDate),
            "password": self.password,
            "firstname": self.firstname,
            "lastname": self.lastname
        }

