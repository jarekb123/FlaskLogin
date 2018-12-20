from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('webapp.config.HerokuConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

db = SQLAlchemy(app)

bcrypt = Bcrypt()


from user.views import ns as user_ns
api.add_namespace(user_ns)
