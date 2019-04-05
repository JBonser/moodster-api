from flask import request
from flask_restplus import Resource, fields, Namespace

from app.users.service import create_new_user


api = Namespace('users', description='user related operations')
user_view_model = api.model('user', {
    'email': fields.String(required=True, description='user email'),
    'password': fields.String(required=True, description='user password')
})


@api.route('/')
class User(Resource):
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(user_view_model, validate=True)
    def post(self):
        """Creates a new user """
        data = request.get_json()
        return create_new_user(data=data)
