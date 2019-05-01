from flask import request
from flask_restplus import Resource

from app.team_members.service import (
    create_new_team_member,
    get_all_team_members
)
from app.teams.view import api
from .schemas import team_member_create_schema, team_member_view_schema


api.models[team_member_create_schema.name] = team_member_create_schema
api.models[team_member_view_schema.name] = team_member_view_schema


@api.route('/<public_id>/members/')
@api.param('public_id', 'The team identifier')
class TeamMembersList(Resource):
    @api.response(200, 'Successfully retrieved all team members')
    @api.response(404, 'Could not find a Team with that id')
    def get(self, public_id):
        """Get all team members by team id."""
        return get_all_team_members(public_id)

    @api.doc('add a user as a team member')
    @api.expect(team_member_create_schema, validate=True)
    def post(self, public_id):
        """Creates a new team member """
        data = request.get_json()
        return create_new_team_member(public_id, data=data)
