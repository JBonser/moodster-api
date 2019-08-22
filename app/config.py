import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

# must provide the env var for postgres db
postgres_uri = os.getenv('DATABASE_URL')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'completely_unsafe_dev_key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = postgres_uri or 'sqlite:///' + os.path.join(
        basedir, 'moodster_dev.db')
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = postgres_uri or 'sqlite:///' + os.path.join(
        basedir, 'moodster_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = postgres_uri


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
