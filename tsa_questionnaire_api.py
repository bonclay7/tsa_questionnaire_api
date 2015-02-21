from resources import api, app
from resources.Authentication import Authentication
from resources.UserServices import UserServices, UserListServices



api.add_resource(UserServices, '/user', '/user/<string:login>')
api.add_resource(UserListServices, '/users')
api.add_resource(Authentication, '/authenticate/', endpoint='authenticate')

if __name__ == '__main__':
    #app.run(debug=True, ssl_context='adhoc')
    app.run(host="0.0.0.0", port=8080, debug=True)
    #app.run(debug=True)