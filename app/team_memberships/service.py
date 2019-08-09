import uuid
from flask_restplus import marshal

from app import db
from app.team_memberships.model import Membership
from app.teams.model import Team
from app.users.model import User
from app.team_roles.model import TeamRole
from .schemas import membership_view_schema


def create_new_membership(team_id, data):
    user_id = data['user_id']
    role_id = data['team_role_id']
    response = {
        'status': 'Failed',
        'message': f'User with id {user_id} does not exist',
    }
    user = User.query.filter_by(public_id=user_id).first()
    if user is None:
        return response, 404

    team = Team.query.filter_by(public_id=team_id).first()
    if team is None:
        response['message'] = f'Team with id {team_id} does not exist'
        return response, 404

    role = TeamRole.query.filter_by(public_id=role_id).first()
    if role is None:
        response['message'] = f'Role with id {role_id} does not exist'
        return response, 404

    found = Membership.query.filter_by(user=user, team=team, role=role).first()
    if found:
        response['message'] = 'The user already has membership' \
                              ' of that role within the team'
        return response, 409

    new_team_member = marshal(
        data=create_membership_in_db(team, user, role),
        fields=membership_view_schema)
    return new_team_member, 201


def create_membership_in_db(team, user, role):
    new_team_member = Membership(
        public_id=str(uuid.uuid4()),
        team=team,
        user=user,
        role=role
    )
    db.session.add(new_team_member)
    db.session.commit()
    return new_team_member


def get_membership(public_id):
    return Membership.query.filter_by(public_id=public_id).first()


def get_all_memberships(team_id):
    team = Team.query.filter_by(public_id=team_id).first()
    if not team:
        response = {
            'status': 'Failed',
            'message': f'The team with id {team_id} does not exist'
        }
        return response, 404
    memberships = Membership.query.all()
    return marshal(
        data=memberships,
        fields=membership_view_schema,
        envelope='data'), 200
