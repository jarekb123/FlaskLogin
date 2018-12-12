from webapp.app import bcrypt, db
from user.models import User
from errors import ResourceAlreadyCreated


def login_user(email, password):
    try:
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            return auth_token.decode()
        else:
            return None
    except Exception:
        return None


def register_user(email, password, language, phone_number, city):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email, password, language, phone_number, city)
        db.session.add(user)
        db.session.commit()
        return user
    else:
        raise ResourceAlreadyCreated()
