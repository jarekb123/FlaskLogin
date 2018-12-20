from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restplus import Api


app = Flask(__name__)
app.config.from_object('webapp.config.HerokuConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')


api = Api(app)

db = SQLAlchemy(app)

bcrypt = Bcrypt()

from user.views import ns as user_ns
api.add_namespace(user_ns)
