from flask_restplus import Resource, fields, Namespace
from app.team_roles.service import get_all_team_roles


api = Namespace('team_roles', description='team role related operations')
team_role_view_model = api.model('team_role', {
    'id': fields.String(attribute='public_id', description='team role id'),
    'name': fields.String(description='team role name')
})


@api.route('/')
class TeamRoleList(Resource):
    @api.response(200, 'team roles successfully retrieved')
    @api.doc('Gets all team roles')
    @api.marshal_with(team_role_view_model, envelope='data')
    def get(self):
        """Get all team roles"""
        return get_all_team_roles()
