import uuid
from flask_restplus import marshal
from app import db
from app.teams.model import Team
from .schemas import team_view_schema


def create_new_team(data):
    team_name = data['name']
    new_team = create_team_in_db(team_name)
    return new_team, 201


def create_team_in_db(team_name):
    new_team = Team(
        public_id=str(uuid.uuid4()),
        name=team_name
    )
    db.session.add(new_team)
    db.session.commit()
    return new_team


def get_team(public_id):
    team = Team.query.filter_by(public_id=public_id).first()
    if not team:
        response = {
            'status': 'Failed',
            'message': f'The team with id {public_id} does not exist'
        }
        return response, 404
    return marshal(data=team, fields=team_view_schema, envelope='data'), 200
