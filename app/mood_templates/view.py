from flask import request
from flask_restplus import Resource, Namespace

from .service import (
    create_new_mood_template,
    get_all_mood_templates,
    get_mood_template,
    get_all_moods_in_template
)
from .schemas import mood_template_view_schema, mood_template_create_schema


api = Namespace('mood_templates', description='mood template operations')
api.models[mood_template_view_schema.name] = mood_template_view_schema
api.models[mood_template_create_schema.name] = mood_template_create_schema


@api.route('/')
class MoodTemplateList(Resource):
    @api.response(200, 'Successfully retrieved all mood templates.')
    @api.marshal_list_with(mood_template_view_schema, envelope='data')
    def get(self):
        """Get all mood templates"""
        return get_all_mood_templates()

    @api.doc('create a new mood template')
    @api.expect(mood_template_create_schema, validate=True)
    @api.response(201, 'Successfully created the mood template.')
    def post(self):
        """Creates a new mood template """
        data = request.get_json()
        return create_new_mood_template(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'mood template identifier')
class MoodTemplate(Resource):
    @api.doc('get mood template')
    @api.response(200, 'Successfully retrieved the mood template.')
    @api.response(404, 'Could not find a Mood Template with that id')
    def get(self, public_id):
        """Get a mood template given its identifier"""
        return get_mood_template(public_id)


@api.route('/<public_id>/moods')
@api.param('public_id', 'mood template identifier')
class MoodTemplateMoodList(Resource):
    @api.doc('get all moods in a mood template')
    @api.response(200, 'Successfully retrieved all moods for a mood template.')
    @api.response(404, 'Could not find a Mood Template with that id')
    def get(self, public_id):
        """Get all moods in a mood template given its identifier"""
        return get_all_moods_in_template(public_id)
