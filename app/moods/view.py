from flask import request
from flask_restplus import Resource, Namespace

from .service import (
    create_new_mood,
    get_all_moods,
    get_mood
)
from .schemas import mood_view_schema, mood_create_schema


api = Namespace('moods', description='mood operations')
api.models[mood_view_schema.name] = mood_view_schema
api.models[mood_create_schema.name] = mood_create_schema


@api.route('/')
class MoodList(Resource):
    @api.response(200, 'Successfully retrieved all moods.')
    @api.marshal_list_with(mood_view_schema, envelope='data')
    def get(self):
        """Get all moods"""
        return get_all_moods()

    @api.doc('create a new mood')
    @api.expect(mood_create_schema, validate=True)
    @api.response(201, 'Successfully created the mood')
    def post(self):
        """Creates a new mood"""
        data = request.get_json()
        return create_new_mood(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'mood identifier')
class Mood(Resource):
    @api.doc('get mood')
    @api.response(200, 'Successfully retrieved the mood.')
    @api.response(404, 'Could not find a Mood with that id')
    def get(self, public_id):
        """Get a mood given its identifier"""
        return get_mood(public_id)
