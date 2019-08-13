from flask_testing import TestCase
from flask_migrate import upgrade, downgrade
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.users.service import create_user_in_db
from app.mood_templates.service import create_mood_template_in_db


class TestMoodTemplateListResource(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        upgrade(x_arg='data=true')
        self.user = create_user_in_db("test@test.com", "password")
        access_token = create_access_token(identity=self.user.id)
        self.headers = {"Authorization": "Bearer {}".format(access_token)}

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg='data=true', revision='base')

    def test_mood_template_post_success(self):
        response = self.client.post(
            '/mood_templates/',
            json={'name': 'test_template_name'}, headers=self.headers
        )
        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual('test_template_name', json_response['name'])
        self.assertIn('id', json_response)

    def test_mood_template_post_fails_with_duplicate_entry(self):
        # First Teams Request
        name = 'test_template_name'
        response = self.client.post(
            '/mood_templates/',
            json={'name': name}, headers=self.headers
        )
        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(name, json_response['name'])
        self.assertIn('id', json_response)

        # Duplicate Request
        response = self.client.post(
            '/mood_templates/',
            json={'name': name}, headers=self.headers
        )
        json_response = response.get_json()

        self.assertEqual(response.status_code, 409)
        self.assertEqual(json_response['status'], 'Failed')
        self.assertEqual(
            json_response['message'], f'A mood template with name {name} already exists')

    def test_mood_template_get_all(self):
        mood_template1 = create_mood_template_in_db('test_template1')
        mood_template2 = create_mood_template_in_db('test_template2')

        response = self.client.get('/mood_templates/', headers=self.headers)
        json_response = response.get_json()
        data = json_response['data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(
            item['id'] == mood_template1.public_id for item in data))
        self.assertTrue(any(
            item['name'] == mood_template1.name for item in data))
        self.assertTrue(any(
            item['id'] == mood_template2.public_id for item in data))
        self.assertTrue(any(
            item['name'] == mood_template2.name for item in data))
