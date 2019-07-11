from sqlalchemy_utils import types as column_types

from app import db


class TeamMemberMood(db.Model):
    """ TeamMemberMood Model for storing moods submitted by a team member """
    __tablename__ = "team_member_mood"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    mood_id = db.Column(db.Integer, db.ForeignKey('mood.id'))
    mood = db.relationship(
        'Mood',
        backref=db.backref('mood', cascade='delete, delete-orphan')
    )
    team_member_id = db.Column(db.Integer, db.ForeignKey('team_member.id'))
    team = db.relationship(
        'TeamMember',
        backref=db.backref('team_member', cascade='delete, delete-orphan')
    )

    def __repr__(self):
        return (
            "<{class_name}("
            "public_id={self.public_id}, "
            "team_member_id={self.team_member_id}, "
            "mood_id={self.mood_id} "
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
