from flask_restplus import fields, Model


team_role_view_schema = Model('team_role', {
    'id': fields.String(attribute='public_id', description='team role id'),
    'name': fields.String(description='team role name')
})
