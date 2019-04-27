from app import db


class TeamMember(db.Model):
    """ Team Member Model for storing team member information """
    __tablename__ = "team_member"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship(
        'Team',
        backref=db.backref('members', cascade='delete, delete-orphan')
    )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'User',
        backref=db.backref('team_membership', cascade='delete, delete-orphan')
    )
    role_id = db.Column(db.Integer, db.ForeignKey('team_role.id'))
    role = db.relationship(
        'TeamRole',
        backref=db.backref('team_roles', cascade='delete, delete-orphan')
    )

    def __repr__(self):
        return (
            "<{class_name}("
            "team_id={self.team_id}, "
            "user_id={self.user_id}, "
            "role_id={self.role_id}"
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
