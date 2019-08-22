from flask_restplus import fields, Model


user_view_schema = Model('user', {
    'id': fields.String(attribute='public_id', description='user id'),
    'email': fields.String(required=True, description='user email')
})

user_post_schema = Model('user', {
    'id': fields.String(attribute='public_id', description='user id'),
    'email': fields.String(required=True, description='user email'),
    'password': fields.String(required=True, description='user password')
})
