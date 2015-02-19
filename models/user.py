__author__ = 'grk'



class User:

    def __init__(self):
        self.login = ""
        self.password = ""
        self.email = ""
        self.creationDate = ""
        self.firstname = ""
        self.lastname = ""
        self._id = ""

    @staticmethod
    def user_from_dict(userDict):
        u = User()
        u.login = userDict['login']
        u.password = userDict['password']
        u.email = userDict['email']
        u.creationDate = userDict['creationDate']
        u.firstname = userDict['firstname']
        u.lastname = userDict['lastname']
        u._id = userDict['_id']
        return u


    def format(self):
        return {
            "_id": self._id,
            "login": self.login,
            "password": self.password,
            "email": self.email,
            "creationDate": self.creationDate,
            "firstname": self.firstname,
            "lastname": self.lastname
        }
