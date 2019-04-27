from flask_testing import TestCase
from flask_migrate import upgrade, downgrade

from app import create_app, db
from app.teams.service import create_team_in_db


class TestTeamResource(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        upgrade(x_arg='data=true')

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg='data=true', revision='base')

    def test_team_get(self):
        team = create_team_in_db('test_team_name')
        response = self.client.get('/teams/'+team.public_id)
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual('test_team_name', data['name'])

    def test_team_get_invalid_id(self):
        response = self.client.get('/teams/my-invalid-id')
        self.assertEqual(response.status_code, 404)
