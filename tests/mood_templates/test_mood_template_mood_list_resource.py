from flask_testing import TestCase
from flask_migrate import upgrade, downgrade
from app import create_app, db
from app.mood_templates.service import create_mood_template_in_db
from app.moods.service import create_mood_in_db
from tests.test_helpers import assert_mood_in_response


class TestMoodsTemplateMoodListResource(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        upgrade(x_arg='data=true')
        self.mood_template = create_mood_template_in_db("test_template")
        self.mood1 = create_mood_in_db("mood1", "#ffffff", self.mood_template)
        self.mood2 = create_mood_in_db("mood2", "#aaaaaa", self.mood_template)

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg='data=true', revision='base')

    def test_mood_template_get_moods_success(self):
        response = self.client.get(
            f'/mood_templates/{self.mood_template.public_id}/moods')
        json_response = response.get_json()
        data = json_response['data']
        self.assertEqual(response.status_code, 200)
        assert_mood_in_response(self, self.mood1, data)
        assert_mood_in_response(self, self.mood2, data)

    def test_mood_template_get_invalid_id(self):
        response = self.client.get('/mood_templates/my-invalid-id/moods')
        self.assertEqual(response.status_code, 404)
