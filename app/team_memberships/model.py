from app import db


class Membership(db.Model):
    """ Membership Model for storing team membership information """
    __tablename__ = "membership"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship(
        'Team',
        backref=db.backref('memberships', cascade='delete, delete-orphan')
    )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User',
        backref=db.backref('memberships', cascade='delete, delete-orphan')
    )
    role_id = db.Column(db.Integer, db.ForeignKey('team_role.id'))
    role = db.relationship(
        'TeamRole',
        backref=db.backref('memberships', cascade='delete, delete-orphan')
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} ("
            f"team_id={self.team_id}, "
            f"user_id={self.user_id}, "
            f"role_id={self.role_id}) >"
        )
