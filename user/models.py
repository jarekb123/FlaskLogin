import datetime
import jwt
from webapp.app import app, db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    language = db.Column(db.String(5), nullable=False, default="en_US")
    phone = db.Column(db.String(10), nullable=True)
    city = db.Column(db.String(255), nullable=True)

    def __init__(self, email, password, language, phone=None, city=None, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password, 10).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.language = language
        self.phone = phone,
        self.city = city

    def encode_auth_token(self, user_id):
        """ Generates Auth Token """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """ Decodes the auth token """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

