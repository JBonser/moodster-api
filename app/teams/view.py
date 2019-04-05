from flask import request
from flask_restplus import Resource, fields, Namespace

from app.teams.service import create_new_team, get_team


api = Namespace('teams', description='team related operations')
team_view_model = api.model('team', {
    'name': fields.String(required=True, description='team name'),
    'public_id': fields.String(description='team identifier')
})


@api.route('/')
class TeamList(Resource):
    @api.response(201, 'Team successfully created.')
    @api.doc('create a new team')
    @api.expect(team_view_model, validate=True)
    def post(self):
        """Creates a new team """
        data = request.get_json()
        return create_new_team(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The team identifier')
@api.response(404, 'Team not found.')
class Team(Resource):
    @api.doc('get team')
    @api.marshal_with(team_view_model)
    def get(self, public_id):
        """Get a team given its identifier"""
        team = get_team(public_id)
        if not team:
            api.abort(404)
        else:
            return team
