from resources import api, app
from resources.Authentication import Authentication


api.add_resource(Authentication, '/authenticate/')

if __name__ == '__main__':
    #app.run(debug=True, ssl_context='adhoc')
    app.run(debug=True)