from flask import request
from flask_restplus import Resource, fields

from app.team_members.service import create_new_team_member
from app.teams.service import get_team
from app.teams.view import api
from app.team_members.model import TeamMember


team_member_post_model = api.model('team_member', {
    'user_id': fields.String(required=True, description='user id'),
    'team_role_id': fields.String(required=True, description='team role id')
})

team_member_get_model = api.model('team_member', {
    'id': fields.String(attribute="public_id", description='member id'),
    'team_id': fields.String(description='team id'),
    'user_id': fields.String(description='user id'),
    'team_role_id': fields.String(description='team role id')
})


@api.route('/<public_id>/members/')
@api.param('public_id', 'The team identifier')
@api.response(404, 'Team not found.')
class TeamMembersList(Resource):
    @api.marshal_list_with(team_member_get_model, envelope='data')
    def get(self, public_id):
        """Get team members by team id."""
        team = get_team(public_id)
        return TeamMember.query.filter_by(team=team).all()

    @api.response(201, 'Team Member successfully added.')
    @api.doc('add a user as a team member')
    @api.expect(team_member_post_model, validate=True)
    def post(self, public_id):
        """Creates a new team member """
        data = request.get_json()
        return create_new_team_member(public_id, data=data)
