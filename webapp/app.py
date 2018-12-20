from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restplus import Api
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object('webapp.config.HerokuConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

api = Api(app)

db = SQLAlchemy(app)

bcrypt = Bcrypt()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add('Access-Control-Allow-Credentials', 'True')
    return response


from user.views import ns as user_ns
api.add_namespace(user_ns)
