from flask import request
from flask_restplus import Resource, Namespace, marshal_with

from .service import create_new_user
from .schemas import user_view_schema, user_create_schema


api = Namespace('users', description='user related operations')
api.models[user_view_schema.name] = user_view_schema
api.models[user_create_schema.name] = user_create_schema


@api.route('/')
class User(Resource):
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(user_create_schema, validate=True)
    @marshal_with(user_view_schema, envelope='data')
    def post(self):
        """Creates a new user """
        data = request.get_json()
        return create_new_user(data=data)
