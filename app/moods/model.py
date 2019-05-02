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
            "<{class_name}("
            "public_id={self.public_id}, "
            "name={self.name}, "
            "colour={self.colour}, "
            "template_id={self.template_id} "
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
