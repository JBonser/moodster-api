from flask_testing import TestCase
from flask_migrate import upgrade, downgrade
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.mood_templates.service import create_mood_template_in_db
from app.users.service import create_user_in_db


class TestMoodTemplateResource(TestCase):
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

    def test_mood_template_get(self):
        mood_template = create_mood_template_in_db("test_template_name")
        response = self.client.get(
            f"/mood_templates/{mood_template.public_id}", headers=self.headers
        )
        data = response.get_json()["data"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual("test_template_name", data["name"])

    def test_mood_template_get_invalid_id(self):
        response = self.client.get(
            "/mood_templates/my-invalid-id", headers=self.headers
        )
        self.assertEqual(response.status_code, 404)
