from flask_testing import TestCase
from flask_migrate import upgrade, downgrade

from app import create_app, db
from app.users.service import create_user_in_db


class TestAuthenticationResource(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        upgrade(x_arg='data=true')
        self.user = create_user_in_db("test@test.com", "password")

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg='data=true', revision='base')

    def test_user_login_success(self):
        json = {
            'email': self.user.email,
            'password': 'password'
        }
        response = self.client.post('/auth/', json=json)
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)

    def test_user_login_invalid_password(self):
        json = {
            'email': self.user.email,
            'password': 'incorrect_password'
        }
        response = self.client.post('/auth/', json=json)
        response_json = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['status'], 'Failed')
        self.assertEqual(response_json['message'], 'Incorrect username or password')

    def test_user_login_invalid_user(self):
        json = {
            'email': 'incorrect_user@users.com',
            'password': 'password'
        }
        response = self.client.post('/auth/', json=json)
        response_json = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['status'], 'Failed')
        self.assertEqual(response_json['message'], 'Incorrect username or password')
