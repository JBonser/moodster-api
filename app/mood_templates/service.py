import uuid
from flask_restplus import marshal
from app import db
from .model import MoodTemplate
from .schemas import mood_template_view_schema
from ..moods.model import Mood
from ..moods.schemas import mood_view_schema


def create_new_mood_template(data):
    name = data['name']
    response = {'status': 'Failed'}

    found = MoodTemplate.query.filter_by(name=name).first()
    if found:
        response['message'] = f'A mood template with name {name} already exists'
        return response, 409

    mood_template = marshal(
        data=create_mood_template_in_db(name),
        fields=mood_template_view_schema
    )
    return mood_template, 201


def create_mood_template_in_db(name):
    mood_template = MoodTemplate(
        public_id=str(uuid.uuid4()),
        name=name
    )
    db.session.add(mood_template)
    db.session.commit()
    return mood_template


def get_all_moods_in_template(public_id):
    mood_template = MoodTemplate.query.filter_by(public_id=public_id).first()
    if not mood_template:
        response = {
            'status': 'Failed',
            'message': f'The mood template with id {public_id} does not exist'
        }
        return response, 404

    moods = Mood.query.filter_by(template=mood_template).all()

    return marshal(
        data=moods,
        fields=mood_view_schema,
        envelope='data'), 200


def get_mood_template(public_id):
    mood_template = MoodTemplate.query.filter_by(public_id=public_id).first()
    if not mood_template:
        response = {
            'status': 'Failed',
            'message': f'The mood template with id {public_id} does not exist'
        }
        return response, 404

    return marshal(
        data=mood_template,
        fields=mood_template_view_schema,
        envelope='data'), 200


def get_all_mood_templates():
    return MoodTemplate.query.all(), 200
