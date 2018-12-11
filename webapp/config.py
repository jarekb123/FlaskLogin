import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = 'sadfdkspof0fa-32mfaosd23-mngnruei23k90f'
    DEVELOPMENT = True
