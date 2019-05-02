from flask_restplus import fields, Model


team_view_schema = Model('team', {
    'id': fields.String(attribute='public_id', description='user id'),
    'name': fields.String(required=True, description='team name')

})

team_create_schema = Model('team', {
    'id': fields.String(attribute='public_id', description='user id'),
    'name': fields.String(required=True, description='team name')
})
