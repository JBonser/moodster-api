from flask import request
from flask_restplus import Resource, Namespace
from app import jwt
from .service import authenticate_user
from ..users.schemas import user_post_schema

api = Namespace('auth', description='authentication operations')
api.models[user_post_schema.name] = user_post_schema


@api.route('/')
class AuthenticationLogin(Resource):
    @api.doc('authenticate a user')
    @api.expect(user_post_schema, validate=True)
    @api.response(200, 'Successfully logged in user.')
    @api.response(401, 'Incorrect username or password')
    def post(self):
        """Logs in a user using email and password"""
        data = request.get_json()
        return authenticate_user(data=data)


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return {
        'status': False,
        'message': 'Missing Authorization Header'
    }, 401
