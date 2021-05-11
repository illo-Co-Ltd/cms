from flask_restplus import Namespace, fields

api_auth = Namespace('auth', description='Authentication API')


class LoginDTO:
    api = api_auth
    model = api.model('login', {
        'userid': fields.String(required=True, description='User ID'),
        'password': fields.String(required=True, description='Password'),
    })


class WhoAmIDTO:
    api = api_auth
    model = api.model('whoami', {
        'userid': fields.String(required=True, description='Unique alphabetical user id'),
        'username': fields.String(required=True, description='Name of the user'),
        'company': fields.String(attribute='company.name', required=True,
                                 description='Name of the company user belongs to'),
    })
