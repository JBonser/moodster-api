import uuid
from flask_restplus import marshal

from app import db
from .model import TeamMemberMood
from app.team_members.model import TeamMember
from app.teams.model import Team
from app.moods.model import Mood
from .schemas import team_member_mood_view_schema

def submit_new_team_member_mood(team_id, data):
    team_member_id = data['team_member_id']
    mood_id = data['mood_id']
    response = {
        'status': 'Failed',
        'message': 'Team with id {} does not exist'.format(team_id),
    }
    
    team = Team.query.filter_by(public_id=team_id).first()
    if team is None:
        return response, 404

    team_member = TeamMember.query.filter_by(public_id=team_member_id).first()
    if team_member is None:
        response['message'] = 'Team Member with id {} does not exist'.format(team_id)
        return response, 404
 
    if team_member.team_id != team.id: #if team member exists but is not a member of submitted team
        response['message'] = 'Team Member with id {} does not belong to Team with id {}'.format(team_member_id, team_id)
        return response, 404
    
    mood = Mood.query.filter_by(public_id=mood_id).first()
    if mood is None:
        response['message'] = 'Mood with id {} does not exist'.format(mood_id)
        return response, 404
    
    new_team_member_mood = marshal(
        data=create_team_member_mood_in_db(team_member, mood),
        fields=team_member_mood_view_schema)
    return new_team_member_mood, 201


def create_team_member_mood_in_db(team_member, mood):
    new_team_member_mood = TeamMemberMood(
        public_id=str(uuid.uuid4()),
        team_member=team_member,
        mood=mood
    )
    db.session.add(new_team_member_mood)
    db.session.commit()
    return new_team_member_mood


def get_all_team_moods(public_id):
    team_moods = TeamMemberMood.query.join(TeamMember).join(Team).filter(Team.public_id == public_id).all()
    return marshal(
            data=team_moods,
            fields=team_member_mood_view_schema,
            envelope='data'), 200
    
    
def get_all_team_member_moods(team_member_id):
    team_member = TeamMember.query.filter_by(public_id=team_member_id).first()
    team_member_moods = TeamMemberMood.query.filter_by(team_member=team_member).all()
    return marshal(
            data=team_member_moods,
            fields=team_member_mood_view_schema,
            envelope='data'), 200

