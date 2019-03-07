from flask import Flask, Blueprint
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import config_by_name


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    Migrate(app, db)

    blueprint = Blueprint('api', __name__)
    api = Api(blueprint, description='Team related operations')

    from app.teams.view import api as team_ns
    api.add_namespace(team_ns)

    app.register_blueprint(blueprint)

    return app
