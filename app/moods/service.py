import uuid
from flask_restplus import marshal
from app import db
from .model import Mood
from ..mood_templates.model import MoodTemplate
from .schemas import mood_view_schema


def create_new_mood(data):
    name = data['name']
    colour = data['colour']
    template_id = data['template_id']
    response = {'status': 'Failed'}

    template = MoodTemplate.query.filter_by(public_id=template_id).first()
    if not template:
        response['message'] = 'The template with id {}'\
                              'does not exist'.format(template_id)
        return response, 404

    mood_template = marshal(
        data=create_mood_in_db(name, colour, template),
        fields=mood_view_schema
    )
    return mood_template, 201


def create_mood_in_db(name, colour, template):
    mood = Mood(
        public_id=str(uuid.uuid4()),
        name=name,
        colour=colour,
        template=template
    )
    db.session.add(mood)
    db.session.commit()
    return mood


def get_mood(public_id):
    mood = Mood.query.filter_by(public_id=public_id).first()
    if not mood:
        response = {
            'status': 'Failed',
            'message': 'The mood with id {} does not exist'.format(public_id)
        }
        return response, 404

    return marshal(
        data=mood,
        fields=mood_view_schema,
        envelope='data'), 200


def get_all_moods():
    return Mood.query.all(), 200
