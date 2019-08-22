from flask_testing import TestCase
from flask_migrate import upgrade, downgrade
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.team_roles.service import get_team_role_by_name
from app.users.service import create_user_in_db


class TestTeamRolesListResource(TestCase):
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

    def test_team_roles_get_default_roles(self):
        response = self.client.get("/team_roles/", headers=self.headers)
        json_response = response.get_json()

        admin_role = get_team_role_by_name('Admin')
        member_role = get_team_role_by_name('Member')

        self.assertEqual(response.status_code, 200)
        data = json_response['data']
        self.assertTrue(any(
            item['id'] == member_role.public_id for item in data))
        self.assertTrue(any(
            item['id'] == admin_role.public_id for item in data))
