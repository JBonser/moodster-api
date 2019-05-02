from flask_restplus import fields, Model
from app.utils.colour_field import ColourField

mood_create_schema = Model('mood_create', {
    'name': fields.String(required=True, description='name'),
    'colour': ColourField(required=True, description='colour'),
    'template_id': fields.String(
        attribute="template.public_id",
        required=True,
        description='template id'),
})

mood_view_schema = Model('mood_view', {
    'id': fields.String(attribute="public_id", description='member id'),
    'name': fields.String(required=True, description='name'),
    'colour': ColourField(required=True, description='colour'),
    'template_id': fields.String(
        attribute="template.public_id",
        required=True,
        description='template id'),
})
