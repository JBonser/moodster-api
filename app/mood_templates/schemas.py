from flask_restplus import fields, Model


mood_template_create_schema = Model('mood_template_get', {
    'name': fields.String(required=True, description='name')
})

mood_template_view_schema = Model('mood_template_post', {
    'id': fields.String(attribute='public_id', description='member id'),
    'name': fields.String(required=True, description='name')
})
