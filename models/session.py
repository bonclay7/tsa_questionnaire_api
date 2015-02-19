__author__ = 'grk'

import datetime
import hashlib
from user import User


class Session:
    def __init__(self):
        self.token = ""
        self.creation_date = datetime.datetime.now()
        self.terminate_date = ""
        self.status = 0
        self.user = None

    @staticmethod
    def session_from_user(user):
        session = Session()
        session.user = user
        session.token = hashlib.sha256(user.login + "." + str(session.creation_date)).hexdigest()
        return session


    @staticmethod
    def session_from_dict(session_dict):
        s = Session()
        s.user = User.user_from_dict(session_dict["user"])
        s.token = session_dict["token"]
        s.creation_date = session_dict["creationDate"]
        s.terminate_date = session_dict["terminateDate"]
        s.status = session_dict["status"]
        return s


    def format(self):
        return {"token": self.token,
                "creationDate": self.creation_date,
                "terminateDate": self.terminate_date,
                "status": self.status,
                "user": self.user.format()}

    def format_http(self):
        return {"token": self.token,
                "creationDate": str(self.creation_date),
                "user": self.user.login}