from flask_testing import TestCase

from app import create_app, db
from app.teams.service import create_team_in_db


class TestTeamResource(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_team_get(self):
        team = create_team_in_db('test_team_name')
        response = self.client.get('/teams/'+team.public_id)
        json_response = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual('test_team_name', json_response['name'])

    def test_team_get_invalid_id(self):
        response = self.client.get('/teams/my-invalid-id')
        json_response = response.get_json()

        self.assertEqual(response.status_code, 404)
