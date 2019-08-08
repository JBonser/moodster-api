from flask_jwt_extended import create_access_token
from flask_restplus import marshal
from ..users.model import User
from .schemas import auth_login_view_schema
from app import bcrypt


def authenticate_user(data):
    email = data['email']
    user = User.query.filter_by(email=email).first()
    response = {
        'status': 'Failed',
        'message': 'Incorrect username or password',
    }

    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return response, 401

    access_token = create_access_token(identity=user.id)
    response['access_token'] = access_token
    response['message'] = 'Successfully logged in user.'
    return marshal(
        data=response,
        fields=auth_login_view_schema,
        envelope='data'
    )
