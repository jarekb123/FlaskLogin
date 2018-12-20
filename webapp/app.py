import os
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


from user.views import ns as user_ns
api.add_namespace(user_ns)

if __name__ == '__main__':
    port = os.getenv("PORT")
    app.run('0.0.0.0', port, debug=True)
