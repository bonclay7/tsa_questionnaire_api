from resources import api, app
from resources.Authentication import Authentication
from resources.QuizResource import QuizResource
from resources.UserServices import UserServices, UserListServices



api.add_resource(Authentication, '/authenticate/', endpoint='authenticate')
api.add_resource(UserServices, '/user/', '/user/<login>', endpoint='user')
api.add_resource(UserListServices, '/users')
api.add_resource(QuizResource, "/quiz/", "/quiz/<quiz_id>")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)