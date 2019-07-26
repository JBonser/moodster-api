from flask_restplus import fields, Model


membership_create_schema = Model('membership_post', {
    'user_id': fields.String(required=True, description='user id'),
    'team_role_id': fields.String(required=True, description='team role id')
})

membership_view_schema = Model('membership_get', {
    'id': fields.String(attribute="public_id", description='member id'),
    'team_id': fields.String(
        attribute="team.public_id", description='team id'),
    'user_id': fields.String(
        attribute="user.public_id", description='user id'),
    'team_role_id': fields.String(
        attribute="role.public_id", description='team role id')
})
