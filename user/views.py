import jwt
from flask_restplus import fields, Resource

from webapp.app import api
from user.service import *

ns = api.namespace('user', description='User related operations')


@ns.errorhandler(jwt.InvalidTokenError)
def handle_invalid_token():
    return {'status': 'fail', 'message': 'Invalid Token'}, 400


@ns.errorhandler(jwt.ExpiredSignatureError)
def handle_token_expired():
    return {'status': 'fail', 'message': 'Token expired'}, 400


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


user_model = ns.model('User Model', {
    'id': fields.Integer(required=False, description='User\'s id'),
    'email': fields.String(required=True),
    'registered_on': fields.DateTime(required=True),
    'language': fields.String(required=True),
    'phone': fields.String(required=True),
    'city': fields.String(required=True)
})

update_user_request = ns.model('Update User Request Model', {
    'email': fields.String(required=True, description='User\'s email address'),
    'password': fields.String(required=False, description='User\'s password'),
    'language': fields.String(required=True, description='User\'s language'),
    'phone': fields.String(required=True, description='User\'s phone number'),
    'city': fields.String(required=True, description='User\'s city')
})

header_parser = ns.parser()
header_parser.add_argument('Authorization', location='headers')


@ns.route('/profile')
class UserResource(Resource):

    @ns.errorhandler(KeyError)
    def handle_key_error(self):
        return {'message': 'Bad request'}, 400

    @ns.errorhandler(ResourceNotExist)
    def handle_no_resource_error(self):
        return {'message': 'User does not exist.'}, 404

    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    @ns.expect(header_parser)
    def get(self):
        """ Get signed in user authenticated by JWT token """
        args = header_parser.parse_args()
        token_header = args['Authorization']
        splitted_token = token_header.split(" ")
        token = splitted_token[1]

        user_id = User.decode_auth_token(token)
        return get_user(user_id)

    @ns.doc("put_user")
    @ns.expect(update_user_request, header_parser)
    @ns.marshal_with(user_model)
    def put(self):
        """ Update current user """
        args = header_parser.parse_args()
        token = args['Authorization'].split(" ")[1]

        user_id = User.decode_auth_token(token)
        return update_user(user_id=user_id, **api.payload)


@ns.route('/logout')
class LogoutResource(Resource):

    @ns.doc('logout_user')
    @ns.expect(header_parser)
    def get(self):
        header_args = header_parser.parse_args()
        token = header_args['Authorization'].split(" ")[1]
        if token:
            if logout_user(token):
                return {'status': 'success'}, 200
            else:
                return {'status': 'fail'}, 500
        else:
            raise jwt.InvalidTokenError()
