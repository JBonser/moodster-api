from flask_testing import TestCase
from flask_migrate import upgrade, downgrade

from app import create_app, db
from app.team_roles.service import get_team_role_by_name


class TestTeamRolesListResource(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        upgrade(x_arg='data=true')

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg='data=true', revision='base')

    def test_team_roles_get_default_roles(self):
        response = self.client.get("/team_roles/")
        json_response = response.get_json()

        admin_role = get_team_role_by_name('Admin')
        member_role = get_team_role_by_name('Member')

        self.assertEqual(response.status_code, 200)
        data = json_response['data']
        self.assertTrue(any(
            item['id'] == member_role.public_id for item in data))
        self.assertTrue(any(
            item['id'] == admin_role.public_id for item in data))
