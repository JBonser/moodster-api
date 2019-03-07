from app import db


class Team(db.Model):
    """ Team Model for storing team related details """
    __tablename__ = "team"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<Team '{}'>".format(self.name)
