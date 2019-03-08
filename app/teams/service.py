import uuid

from app import db
from app.teams.model import Team


def create_new_team(data):
    new_team = create_team_in_db(data)
    response_object = {
        'status': 'Success',
        'message': 'Successfully created team.',
        'team_id': new_team.public_id,
        'name': new_team.name
    }
    return response_object, 201


def create_team_in_db(data):
    new_team = Team(
        public_id=str(uuid.uuid4()),
        name=data['name']
    )
    db.session.add(new_team)
    db.session.commit()
    return new_team


def get_team(public_id):
    return Team.query.filter_by(public_id=public_id).first()
