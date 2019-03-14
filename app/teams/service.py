import uuid

from app import db
from app.teams.model import Team


def create_new_team(data):
    team_name = data['name']
    new_team = create_team_in_db(team_name)
    response = {
        'status': 'Success',
        'message': 'Successfully created team.',
        'team_id': new_team.public_id,
        'name': new_team.name
    }
    return response, 201


def create_team_in_db(team_name):
    new_team = Team(
        public_id=str(uuid.uuid4()),
        name=team_name
    )
    db.session.add(new_team)
    db.session.commit()
    return new_team


def get_team(public_id):
    return Team.query.filter_by(public_id=public_id).first()
