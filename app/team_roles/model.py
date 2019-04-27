from app import db


class TeamRole(db.Model):
    """ Team Role Model for storing team role information """
    __tablename__ = "team_role"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return (
            "<{class_name}("
            "id={self.id}, "
            "public_id={self.public_id}, "
            "name={self.name}"
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
