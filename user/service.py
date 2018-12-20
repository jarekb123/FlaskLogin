from webapp.app import bcrypt, db
from user.models import User, BlacklistToken
from errors import ResourceAlreadyCreated, ResourceNotExist


def register_user(email, password, language, phone_number, city):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email, password, language, phone_number, city)
        db.session.add(user)
        db.session.commit()
        return user
    else:
        raise ResourceAlreadyCreated()


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


def logout_user(token):
    resp = User.decode_auth_token(token)
    if not isinstance(resp, str):  # if resp is str, it means that token is corrupted or expired
        blacklist_token = BlacklistToken(token=token)
        try:
            db.session.add(blacklist_token)
            db.session.commit()
            return True
        except:
            return False
    else:
        return False


def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user
    else:
        raise ResourceNotExist()


def update_user(user_id, **kwargs):
    user = User.query.get(user_id)
    if user:
        user.email = kwargs['email']
        user.language = kwargs['language']
        user.phone = kwargs['phone']
        user.city = kwargs['city']

        if kwargs.get('password'):
            user.password = User.generate_password_hash(kwargs['password'])
        db.session.commit()
        return user
    else:
        raise ResourceNotExist()
