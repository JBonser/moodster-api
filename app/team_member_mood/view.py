from flask import request
from flask_restplus import Resource, Namespace, marshal_with


from .service import submit_new_team_member_mood, get_all_team_member_moods, get_all_team_moods
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
    def post(self, public_id):
        """Submits a team members mood """
        data = request.get_json()
        return submit_new_team_member_mood(public_id, data=data)


@api.route('/<public_id>/team_member_mood')
@api.param('public_id', 'The team identifier')
class TeamMoodList(Resource):
    @api.doc('get all moods submitted by a team member')
    @api.response(200, 'Successfully retrieved all submitted moods for a team')
    @api.response(404, 'Could not find a team with that id')
    def get(self, public_id):
        """Get all submitted moods by a team given its identifier"""
        return get_all_team_moods(public_id)


@api.route('/<public_id>/team_member_mood/<team_member_id>')
@api.param('public_id', 'The team identifier')
@api.param('team_member_id', 'The team member identifier')
class TeamMemberMoodList(Resource):
    @api.doc('get all moods submitted by a team member')
    @api.response(200, 'Successfully retrieved all submitted moods for a team member.')
    @api.response(404, 'Could not find a team member with that id')
    def get(self, public_id, team_member_id):
        """Get all submitted moods by a team member given its identifier"""
        return get_all_team_member_moods(team_member_id)
