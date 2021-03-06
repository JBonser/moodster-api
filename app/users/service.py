import uuid
from app import db, bcrypt
from .model import User


def create_new_user(data):
    email = data['email']
    password = data['password']

    new_user = create_user_in_db(email, password)
    return new_user, 201


def create_user_in_db(email, password):
    hash_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(
        public_id=str(uuid.uuid4()),
        email=email,
        password=hash_pw
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


def get_user(public_id):
    return User.query.filter_by(public_id=public_id).first()
