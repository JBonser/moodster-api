from flask_testing import TestCase
from flask_migrate import upgrade, downgrade

from app import create_app, db
from app.teams.service import create_team_in_db
from app.users.service import create_user_in_db
from app.team_roles.service import get_team_role_by_name
from app.team_members.service import create_team_member_in_db


class TestTeamMembersListResource(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        upgrade(x_arg='data=true')
        self.test_team1 = create_team_in_db('test_team_name')
        self.test_team2 = create_team_in_db('test_team_name2')
        self.test_user1 = create_user_in_db("test_user1@test.com", "password")
        self.test_user2 = create_user_in_db("test_user2@test.com", "password")
        self.admin_role = get_team_role_by_name('Admin')
        self.member_role = get_team_role_by_name('Member')

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg='data=true', revision='base')

    def test_team_members_post_single_member_addition(self):
        response = self.send_team_members_post(
            self.test_team1.public_id,
            self.member_role.public_id,
            self.test_user1.public_id)

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(
            json_response['message'], 'Successfully created team member')
        self.assertIn('team_member_id', json_response)

    def test_team_members_post_fails_with_invalid_role(self):
        response = self.send_team_members_post(
            self.test_team1.public_id,
            'invalid_id',
            self.test_user1.public_id)

        json_response = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response['status'], 'Failed')
        self.assertEqual(
            json_response['message'], 'Role with id invalid_id does not exist')

    def test_team_members_post_fails_with_invalid_user(self):
        response = self.send_team_members_post(
            self.test_team1.public_id,
            self.member_role.public_id,
            'invalid_id')

        json_response = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response['status'], 'Failed')
        self.assertEqual(
            json_response['message'], 'User with id invalid_id does not exist')

    def test_team_members_post_fails_with_invalid_team_url(self):
        response = self.send_team_members_post(
            'invalid_team_url',
            self.member_role.public_id,
            self.test_user1.public_id)

        json_response = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response['status'], 'Failed')
        self.assertEqual(
            json_response['message'],
            'Team with id invalid_team_url does not exist')

    def test_team_members_post_fails_with_duplicate_entry(self):
        # First Teams Request
        response = self.send_team_members_post(
            self.test_team1.public_id,
            self.member_role.public_id,
            self.test_user1.public_id)

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(
            json_response['message'], 'Successfully created team member')
        self.assertIn('team_member_id', json_response)

        # Duplicate Request
        response = self.send_team_members_post(
            self.test_team1.public_id,
            self.member_role.public_id,
            self.test_user1.public_id)

        json_response = response.get_json()

        self.assertEqual(response.status_code, 409)
        self.assertEqual(json_response['status'], 'Failed')
        self.assertEqual(
            json_response['message'],
            'The user already has membership of that role within the team')

    def test_team_members_post_success_for_multiple_roles_within_a_team(self):
        # Member Role Request
        response = self.send_team_members_post(
            self.test_team1.public_id,
            self.member_role.public_id,
            self.test_user1.public_id)

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(
            json_response['message'], 'Successfully created team member')
        self.assertIn('team_member_id', json_response)

        # Admin Role Request
        response = self.send_team_members_post(
            self.test_team1.public_id,
            self.admin_role.public_id,
            self.test_user1.public_id)

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(
            json_response['message'], 'Successfully created team member')
        self.assertIn('team_member_id', json_response)

    def test_team_members_post_success_for_multiple_teams(self):
        # First Teams Request
        response = self.send_team_members_post(
            self.test_team1.public_id,
            self.member_role.public_id,
            self.test_user1.public_id)

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(
            json_response['message'], 'Successfully created team member')
        self.assertIn('team_member_id', json_response)

        # Second Teams Request
        response = self.send_team_members_post(
            self.test_team2.public_id,
            self.member_role.public_id,
            self.test_user1.public_id)

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response['status'], 'Success')
        self.assertEqual(
            json_response['message'], 'Successfully created team member')
        self.assertIn('team_member_id', json_response)

    def test_team_members_get(self):
        team_member1 = create_team_member_in_db(
            self.test_team1, self.test_user1, self.member_role)
        team_member2 = create_team_member_in_db(
            self.test_team1, self.test_user2, self.member_role)

        response = self.client.get("/teams/{}/members/".format(
                self.test_team1.public_id))
        data = response.get_json()['data']

        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(
            item['id'] == team_member1.public_id for item in data))
        self.assertTrue(any(
            item['id'] == team_member2.public_id for item in data))

    def send_team_members_post(self, team_id, role_id, user_id):
        team_member = {
            'user_id': user_id,
            'team_role_id': role_id
        }
        return self.client.post("/teams/{}/members/".format(
                team_id), json=team_member)
