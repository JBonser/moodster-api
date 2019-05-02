from flask_restplus import Resource, Namespace
from .service import get_all_team_roles
from .schemas import team_role_view_schema


api = Namespace('team_roles', description='team role related operations')
api.models[team_role_view_schema.name] = team_role_view_schema


@api.route('/')
class TeamRoleList(Resource):
    @api.response(200, 'Team roles successfully retrieved')
    @api.doc('Gets all team roles')
    @api.marshal_with(team_role_view_schema, envelope='data')
    def get(self):
        """Get all team roles"""
        return get_all_team_roles()
