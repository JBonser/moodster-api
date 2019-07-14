from app import db


class MoodTemplate(db.Model):
    """ Mood Template Model for storing types of mood templates"""

    __tablename__ = "mood_template"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} ("
            f"public_id={self.public_id}, "
            f"name={self.name} )>"
        )
