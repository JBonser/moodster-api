from flask_testing import TestCase
from flask_migrate import upgrade, downgrade
from app import create_app, db
from app.moods.service import create_mood_in_db
from app.mood_templates.service import create_mood_template_in_db
from tests.test_helpers import assert_mood_in_response


class TestMoodListResource(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        upgrade(x_arg='data=true')
        self.template = create_mood_template_in_db('test_template')

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg='data=true', revision='base')

    def test_mood_post_success(self):
        json = {
            'name': 'test_mood',
            'colour': '#ff2233',
            'template_id': self.template.public_id
        }
        response = self.client.post('/moods/', json=json)
        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual('test_mood', json_response['name'])
        self.assertEqual('#ff2233', json_response['colour'])
        self.assertEqual(self.template.public_id, json_response['template_id'])
        self.assertIn('id', json_response)

    def test_mood_post_invalid_template(self):
        json = {
            'name': 'test_mood',
            'colour': '#ff2233',
            'template_id': 'invalid_template'
        }
        response = self.client.post('/moods/', json=json)
        json_response = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertIn('does not exist', json_response['message'])

    def test_mood_get_all(self):
        mood1 = create_mood_in_db('test_mood1', '#112233', self.template)
        mood2 = create_mood_in_db('test_mood2', '#654321', self.template)

        response = self.client.get('/moods/')
        json_response = response.get_json()
        data = json_response['data']

        self.assertEqual(response.status_code, 200)
        assert_mood_in_response(self, mood1, data)
        assert_mood_in_response(self, mood2, data)
