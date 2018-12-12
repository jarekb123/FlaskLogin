from flask_restplus import fields, Resource

from webapp.app import api
from user.service import *

ns = api.namespace('auth', description='Auth operations')

login_request = ns.model('Login request', {
    'email': fields.String(description='User\'s e-mail address'),
    'password': fields.String(description='Users\'s password')
})

login_response = ns.model('Login response', {
    'status': fields.String(description='Login request status'),
    'auth_token': fields.String(required=False, description='Auth token'),
})


class LoginResponse:
    def __init__(self, status, auth_token=None):
        self.status = status
        self.auth_token = auth_token


@ns.route('/login')
class LoginResource(Resource):

    @ns.doc('post_login')
    @ns.expect(login_request)
    @ns.marshal_with(login_response)
    def post(self):
        """ Login user to the app """
        data = api.payload
        token = login_user(data['email'], data['password'])
        if token:
            return LoginResponse('success', token), 200
        return LoginResponse('fail'), 500


register_request = ns.model('Register request', {
    'email': fields.String(required=True, description='User\'s email address'),
    'password': fields.String(required=True, description='User\'s password'),
    'lang': fields.String(required=True, description='User\'s language'),
    'phone': fields.String(required=False, description='User\'s phone number'),
    'city': fields.String(required=False, description='Users\'s city')
})

register_response = ns.model('Register response', {
    'status': fields.String()
})


class RegisterResponse:
    def __init__(self, status):
        self.status = status


@ns.route('/register')
class RegisterResource(Resource):

    @ns.doc('register_post')
    @ns.expect(register_request)
    @ns.marshal_with(register_response)
    def post(self):
        """ Register user in the app """
        data = api.payload
        user = register_user(data['email'], data['password'], data.get('lang'), data.get('phone'), data.get('city'))
        if user:
            return RegisterResponse('success'), 201

    @ns.errorhandler(ResourceAlreadyCreated)
    @ns.marshal_with(register_response, code=202)
    def handle_user_already_registered(self):
        """ Handler: User already registered """
        return RegisterResponse('user_already_exist'), 202


user_response = ns.model('User Model', {
    'id': fields.Integer(),
    'email': fields.String(),
    'registered_on': fields.DateTime(),
    'language': fields.String(),
    'phone': fields.String(),
    'city': fields.String()
})

header_parser = ns.parser()
header_parser.add_argument('Authentication', location='headers')


@ns.route('/user')
class UserResource(Resource):

    @ns.doc('get_user')
    @ns.marshal_with(user_response)
    @ns.expect(header_parser)
    def get(self):
        args = header_parser.parse_args()
        token_header = args['Authentication']
        splitted_token = token_header.split(" ")
        token = splitted_token[1]

        print(token)

        user_id = User.decode_auth_token(token)
        return User.query.get(user_id)






