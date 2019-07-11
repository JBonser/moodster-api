from flask import request
from flask_restplus import Resource, Namespace, marshal_with


from .service import submit_new_team_member_mood
from .schemas import team_member_mood_view_schema, team_member_mood_post_schema

from app.teams.view import api

api.models[team_member_mood_view_schema.name] = team_member_mood_view_schema
api.models[team_member_mood_post_schema.name] = team_member_mood_post_schema

@api.route('/<public_id>/team_member_mood/')
@api.param('public_id', 'The team identifier')
class TeamMemberMood(Resource):
    @api.response(201, 'Team Member Mood successfully submitted.')
    @api.response(404, 'Error submitting Team Member Mood.')
    @api.doc('submit a team member mood')
    @api.expect(team_member_mood_post_schema, validate=True)
    @marshal_with(team_member_mood_view_schema, envelope='data')
    def post(self, public_id):
        """Submits a team members mood """
        data = request.get_json()
        return submit_new_team_member_mood(public_id, data=data)
