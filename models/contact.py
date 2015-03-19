__author__ = 'grk'
from flask.ext.restful import reqparse, fields
from validate_email import validate_email

def email(email_str):
    if validate_email(email_str):
        return email_str
    return None



contact_fields = {
    'firstname': fields.String,
    'lastname': fields.String,
    'email': fields.String,
    'language': fields.String,
    'creationDate': fields.DateTime
}

post_parser = reqparse.RequestParser()

post_parser.add_argument('contacts', dest='contacts', type=list, location='json', required=True, )
post_parser.add_argument('contacts.language', type=list, location='json', required=False, help='language is missing', )
post_parser.add_argument('contacts.firstname', dest='contacts.firstname', type=list, location='json', required=False, )
post_parser.add_argument('contacts.lastname', dest='contacts.lastname', type=list, location='json', required=False, )
post_parser.add_argument('contacts.email', dest='contacts.email', type=email, location='json', required=False, help='The user\'s email', )


class Contact:
    def __init__(self):
        self.language = ""
        self.firstname = ""
        self.lastname = ""
        self.email = ""
        self.creationDate = ""
        self.createdBy = ""
        self._id = ""

    @staticmethod
    def contact_from_dict(userDict):
        c = Contact()
        c.language = userDict.get('language')
        c.creationDate = userDict.get('creationDate')
        c.firstname = userDict.get('firstname')
        c.lastname = userDict.get('lastname')
        c.email = userDict.get('email')
        c.createdBy = userDict.get('createdBy')
        c._id = userDict.get('_id')
        return c


    def format(self):
        return {
            "_id": self._id,
            "language": self.language,
            "email": self.email,
            "creationDate": str(self.creationDate),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "createdBy": self.createdBy
        }

    def format_for_update(self):
        return {
            "language": self.language,
            "email": self.email,
            "creationDate": str(self.creationDate),
            "firstname": self.firstname,
            "lastname": self.lastname
        }

    def format_for_delete(self):
        return {
            "_id": self._id,
            "language": self.language,
            "email": self.email,
            "creationDate": str(self.creationDate),
            "firstname": self.firstname,
            "lastname": self.lastname,
            "deleteDate": str(self.deleteDate)
        }

    def format_for_create(self):
        return {
            "language": self.language,
            "email": self.email,
            "creationDate": str(self.creationDate),
            "firstname": self.firstname,
            "lastname": self.lastname
        }

