from sqlalchemy_utils import ColorType

from app import db


class Mood(db.Model):
    """ Mood Model for storing types of moods"""
    __tablename__ = "mood"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    colour = db.Column(ColorType, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('mood_template.id'))
    template = db.relationship(
        'MoodTemplate',
        backref=db.backref('moods', cascade='delete, delete-orphan')
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} ("
            f"public_id={self.public_id}, "
            f"name={self.name}, "
            f"colour={self.colour}, "
            f"template_id={self.template_id}) >"
        )
