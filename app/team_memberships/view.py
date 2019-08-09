from flask import request
from flask_restplus import Resource

from app.team_memberships.service import (
    create_new_membership,
    get_all_memberships
)
from app.teams.view import api
from .schemas import membership_create_schema, membership_view_schema


api.models[membership_create_schema.name] = membership_create_schema
api.models[membership_view_schema.name] = membership_view_schema


@api.route('/<public_id>/memberships/')
@api.param('public_id', 'The team identifier')
class TeamMembershipsList(Resource):
    @api.doc('Get all memberships for the team')
    @api.response(200, 'Successfully retrieved all memberships')
    @api.response(404, 'Could not find a Team with that id')
    def get(self, public_id):
        """Get all memberships by team id."""
        return get_all_memberships(public_id)

    @api.doc('add membership to the team')
    @api.expect(membership_create_schema, validate=True)
    def post(self, public_id):
        """Adds a team membership """
        data = request.get_json()
        return create_new_membership(public_id, data=data)
