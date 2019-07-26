from flask import Flask, Blueprint
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import config_by_name


db = SQLAlchemy(session_options={'expire_on_commit': False})
migrate = Migrate()


def create_app(config_name):
    app_ = Flask(__name__)
    app_.config.from_object(config_by_name[config_name])
    db.init_app(app_)
    migrate.init_app(app_, db)

    blueprint = Blueprint('api', __name__)
    api = Api(blueprint, description='Moodster API')

    from app.teams.view import api as team_ns
    from app.users.view import api as user_ns
    from app.team_memberships.view import api as team_membership_ns
    from app.team_member_moods.view import api as team_member_mood_ns
    from app.team_roles.view import api as team_role_ns
    from app.mood_templates.view import api as mood_template_ns
    from app.moods.view import api as mood_ns
    api.add_namespace(team_ns)
    api.add_namespace(user_ns)
    api.add_namespace(team_membership_ns)
    api.add_namespace(team_member_mood_ns)
    api.add_namespace(team_role_ns)
    api.add_namespace(mood_template_ns)
    api.add_namespace(mood_ns)

    app_.register_blueprint(blueprint)

    return app_
