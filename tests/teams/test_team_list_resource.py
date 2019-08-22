from flask_testing import TestCase
from flask_migrate import upgrade, downgrade
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.users.service import create_user_in_db


class TestTeamListResource(TestCase):
    def create_app(self):
        return create_app("test")

    def setUp(self):
        upgrade(x_arg="data=true")
        self.user = create_user_in_db("test@test.com", "password")
        access_token = create_access_token(identity=self.user.id)
        self.headers = {"Authorization": "Bearer {}".format(access_token)}

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg="data=true", revision="base")

    def test_team_creation(self):
        response = self.client.post(
            "/teams/", json={"name": "test_team_name"}, headers=self.headers
        )
        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual("test_team_name", json_response["name"])
        self.assertIn("id", json_response)

    def test_team_creation_no_name(self):
        response = self.client.post("/teams/", json={}, headers=self.headers)
        json_response = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("payload validation failed", json_response["message"])
        self.assertIn("name", json_response["errors"])
