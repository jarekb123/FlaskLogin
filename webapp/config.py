import os

db_name = "login"
postgres_local_base = 'postgresql://postgres:postgres@localhost:5433/' + db_name


class Config:
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')


class HerokuConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('HEROKU_POSTGRESQL_MAROON_URL')
    DEVELOPMENT = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = postgres_local_base + '_dev'
    DEVELOPMENT = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = postgres_local_base + '_test'
    DEBUG = True
    TESTING = True
