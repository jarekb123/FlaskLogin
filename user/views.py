from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from webapp.app import app, db
from user.models import User

auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """ User Registration Endpoint """

    def post(self):
        post_data = request.get_json()

        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )
                db.session.add(user)
                db.session.commit()

                auth_token = user.encode_auth_token(user.id)
                responseObj = {
                    'status': 'success',
                    'message': 'Successfully registered',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObj)), 201
            except Exception as e:
                responseObj = {
                    'status': 'fail',
                    'message': 'Error occured. Please try again'
                }
                return make_response(jsonify(responseObj)), 401
        else:
            responseObj = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.'
            }
            return make_response(jsonify(responseObj)), 202


registration_view = RegisterAPI.as_view('register_api')
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)


class LoginAPI(MethodView):
    """ User Login Resource """

    def post(self):
        post_data = request.get_json()
        try:
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_obj = {
                    'status': 'success',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(response_obj)), 200
        except Exception as e:
            print(e)
            response_obj = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(response_obj)), 500


login_view = LoginAPI.as_view('login_api')
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
