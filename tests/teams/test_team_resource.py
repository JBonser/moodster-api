from flask_testing import TestCase
from flask_migrate import upgrade, downgrade
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.users.service import create_user_in_db
from app.teams.service import create_team_in_db


class TestTeamResource(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        upgrade(x_arg='data=true')
        self.user = create_user_in_db("test@test.com", "password")
        access_token = create_access_token(identity=self.user.id)
        self.headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg='data=true', revision='base')

    def test_team_get_success(self):
        team = create_team_in_db('test_team_name')
        response = self.client.get('/teams/'+team.public_id, headers=self.headers)
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertEqual('test_team_name', data['name'])

    def test_team_get_fails_with_invalid_id(self):
        team_id = 'my-invalid-id'
        response = self.client.get(f'/teams/{team_id}', headers=self.headers)
        json_response = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response['status'], 'Failed')
        self.assertEqual(
            json_response['message'],
            f'The team with id {team_id} does not exist')
