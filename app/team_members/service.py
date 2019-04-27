import uuid

from app import db
from app.team_members.model import TeamMember
from app.teams.model import Team
from app.users.model import User
from app.team_roles.model import TeamRole


def create_new_team_member(team_id, data):
    user_id = data['user_id']
    role_id = data['team_role_id']
    response = {
        'status': 'Failed',
        'message': 'User with id {} does not exist'.format(user_id),
    }
    user = User.query.filter_by(public_id=user_id).first()
    if user is None:
        return response, 404

    team = Team.query.filter_by(public_id=team_id).first()
    if team is None:
        response['message'] = 'Team with id {} does not exist'.format(team_id)
        return response, 404

    role = TeamRole.query.filter_by(public_id=role_id).first()
    if role is None:
        response['message'] = 'Role with id {} does not exist'.format(role_id)
        return response, 404

    found = TeamMember.query.filter_by(user=user, team=team, role=role).first()
    if found:
        response['message'] = 'The user already has membership' \
                              ' of that role within the team'
        return response, 409

    new_team_member = create_team_member_in_db(team, user, role)
    response = {
        'status': 'Success',
        'message': 'Successfully created team member',
        'team_member_id': new_team_member.public_id
    }
    return response, 201


def create_team_member_in_db(team, user, role):
    new_team_member = TeamMember(
        public_id=str(uuid.uuid4()),
        team=team,
        user=user,
        role=role
    )
    db.session.add(new_team_member)
    db.session.commit()
    return new_team_member


def get_team_member(public_id):
    return TeamMember.query.filter_by(public_id=public_id).first()
