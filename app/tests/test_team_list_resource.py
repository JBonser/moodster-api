from flask_testing import TestCase

from app import create_app, db


class TestTeamListResource(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_team_creation(self):
        data = {
            'name': 'test_team_name'
        }
        response = self.client.post('/teams/', json=data)
        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual('test_team_name', json_response['name'])
        self.assertEqual('Success', json_response['status'])
