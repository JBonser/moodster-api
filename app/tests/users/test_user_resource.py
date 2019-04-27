from flask_testing import TestCase
from flask_migrate import upgrade, downgrade

from app import create_app, db


class TestUserResource(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        upgrade(x_arg='data=true')

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg='data=true', revision='base')

    def test_user_creation(self):
        data = {
            'email': 'test@test.co.uk',
            'password': 'password123'
        }
        response = self.client.post('/users/', json=data)
        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['email'], json_response['email'])
        self.assertEqual('Success', json_response['status'])
        self.assertIsNotNone(json_response['user_id'])
