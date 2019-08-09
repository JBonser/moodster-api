from app import db


class TeamMemberMood(db.Model):
    """ TeamMemberMood Model for storing moods submitted by a team member """

    __tablename__ = "team_member_mood"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    mood_id = db.Column(db.Integer, db.ForeignKey("mood.id"))
    mood = db.relationship(
        "Mood", backref=db.backref("mood", cascade="delete, delete-orphan")
    )
    team_member_id = db.Column(db.Integer, db.ForeignKey("membership.id"))
    team_member = db.relationship(
        "Membership", backref=db.backref("team_member", cascade="delete, delete-orphan")
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name___} ("
            f"public_id={self.public_id}, "
            f"team_member_id={self.team_member_id}, "
            f"mood_id={self.mood_id}) >"
        )
