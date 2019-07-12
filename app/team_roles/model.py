from app import db


class TeamRole(db.Model):
    """ Team Role Model for storing team role information """
    __tablename__ = "team_role"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} ("
            f"id={self.id}, "
            f"public_id={self.public_id}, "
            f"name={self.name}) >"
        )
