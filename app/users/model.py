from app import db


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(length=120), unique=True, nullable=False)
    password = db.Column(db.String(length=128), nullable=False)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} ("
            f"public_id={self.public_id}, "
            f"email={self.email}, "
        )
