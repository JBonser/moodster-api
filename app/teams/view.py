from flask import request
from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required
from .service import create_new_team, get_team
from .schemas import team_view_schema, team_create_schema


api = Namespace('teams', description='team related operations')
api.models[team_view_schema.name] = team_view_schema
api.models[team_create_schema.name] = team_create_schema


@api.route('/')
class TeamList(Resource):
    @api.doc('create a new team')
    @api.expect(team_create_schema, validate=True)
    @api.marshal_with(team_view_schema)
    def post(self):
        """Creates a new team """
        data = request.get_json()
        return create_new_team(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The team identifier')
class Team(Resource):
    @api.doc('get team')
    @api.response(404, 'Could not find a Team with that id')
    @jwt_required
    def get(self, public_id):
        """Get a team given its identifier"""
        return get_team(public_id)
