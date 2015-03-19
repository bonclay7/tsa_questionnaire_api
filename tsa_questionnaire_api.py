from resources import api, app
from resources.Authentication import Authentication
from resources.QuizResource import QuizResource
from resources.UserServices import UserServices
from resources.ContactsResource import ContactsServices



api.add_resource(Authentication, '/authenticate/', endpoint='authenticate')
api.add_resource(UserServices, '/users/', '/users/<login>', endpoint='user')
api.add_resource(QuizResource, "/quiz/", "/quiz/<quiz_id>", "/quiz/<quiz_id>/<question_id>", endpoint="quiz")
api.add_resource(ContactsServices, "/contacts/", "/contacts/<group_name>", "/contacts/<group_name>/id/<contact_id>", endpoint="contact")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)