import uuid

from app import db
from app.users.model import User


def create_new_user(data):
    email = data['email']
    password = data['password']
    new_user = create_user_in_db(email, password)
    response = {
        'status': 'Success',
        'message': 'Successfully created user',
        'user_id': new_user.public_id,
        'email': new_user.email
    }
    return response, 201


def create_user_in_db(email, password):
    new_user = User(
        public_id=str(uuid.uuid4()),
        email=email,
        password=password
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user


def get_user(public_id):
    return User.query.filter_by(public_id=public_id).first()