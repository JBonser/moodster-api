import os

basedir = os.path.abspath(os.path.dirname(__file__))

# must provide the env var for postgres db or local sqlite version
# will be used.
postgres_local_base = os.getenv(
    'DATABASE_URL',
    default='sqlite:///' + os.path.join(basedir, 'moodster_prod.db'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'completely_unsafe_dev_key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'moodster_dev.db')


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'moodster_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
