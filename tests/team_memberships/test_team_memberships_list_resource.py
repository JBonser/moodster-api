from flask_testing import TestCase
from flask_migrate import upgrade, downgrade
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.teams.service import create_team_in_db
from app.users.service import create_user_in_db
from app.team_roles.service import get_team_role_by_name
from app.team_memberships.service import create_membership_in_db


class TestTeamMembershipsListResource(TestCase):
    def create_app(self):
        return create_app("test")

    def setUp(self):
        upgrade(x_arg="data=true")
        self.test_team1 = create_team_in_db("test_team_name")
        self.test_team2 = create_team_in_db("test_team_name2")
        self.test_user1 = create_user_in_db("test_user1@test.com", "password")
        self.test_user2 = create_user_in_db("test_user2@test.com", "password")
        self.admin_role = get_team_role_by_name("Admin")
        self.member_role = get_team_role_by_name("Member")
        access_token = create_access_token(identity=self.test_user1.id)
        self.headers = {"Authorization": "Bearer {}".format(access_token)}

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg="data=true", revision="base")

    def test_team_memberships_post_single_member_addition(self):
        response = self.send_team_memberships_post(
            self.test_team1.public_id,
            self.member_role.public_id,
            self.test_user1.public_id,
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json_response)
        self.assertEqual(json_response["team_id"], self.test_team1.public_id)
        self.assertEqual(json_response["team_role_id"], self.member_role.public_id)
        self.assertEqual(json_response["user_id"], self.test_user1.public_id)

    def test_team_memberships_post_fails_with_invalid_role(self):
        invalid_id = "invalid_role_id"
        response = self.send_team_memberships_post(
            self.test_team1.public_id, invalid_id, self.test_user1.public_id
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response["status"], "Failed")
        self.assertEqual(
            json_response["message"], f"Role with id {invalid_id} does not exist"
        )

    def test_team_memberships_post_fails_with_invalid_user(self):
        invalid_id = "invalid_user_id"
        response = self.send_team_memberships_post(
            self.test_team1.public_id, self.member_role.public_id, invalid_id
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response["status"], "Failed")
        self.assertEqual(
            json_response["message"], f"User with id {invalid_id} does not exist"
        )

    def test_team_memberships_post_fails_with_invalid_team_url(self):
        invalid_id = "invalid_team_url"
        response = self.send_team_memberships_post(
            invalid_id, self.member_role.public_id, self.test_user1.public_id
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response["status"], "Failed")
        self.assertEqual(
            json_response["message"], f"Team with id {invalid_id} does not exist"
        )

    def test_team_memberships_post_fails_with_duplicate_entry(self):
        # First Teams Request
        response = self.send_team_memberships_post(
            self.test_team1.public_id,
            self.member_role.public_id,
            self.test_user1.public_id,
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json_response)
        self.assertEqual(json_response["team_id"], self.test_team1.public_id)
        self.assertEqual(json_response["team_role_id"], self.member_role.public_id)
        self.assertEqual(json_response["user_id"], self.test_user1.public_id)

        # Duplicate Request
        response = self.send_team_memberships_post(
            self.test_team1.public_id,
            self.member_role.public_id,
            self.test_user1.public_id,
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 409)
        self.assertEqual(json_response["status"], "Failed")
        self.assertEqual(
            json_response["message"],
            "The user already has membership of that role within the team",
        )

    def test_team_memberships_post_success_for_multiple_roles_within_a_team(self):
        # Member Role Request
        response = self.send_team_memberships_post(
            self.test_team1.public_id,
            self.member_role.public_id,
            self.test_user1.public_id,
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json_response)
        self.assertEqual(json_response["team_id"], self.test_team1.public_id)
        self.assertEqual(json_response["team_role_id"], self.member_role.public_id)
        self.assertEqual(json_response["user_id"], self.test_user1.public_id)

        # Admin Role Request
        response = self.send_team_memberships_post(
            self.test_team1.public_id,
            self.admin_role.public_id,
            self.test_user1.public_id,
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json_response)
        self.assertEqual(json_response["team_id"], self.test_team1.public_id)
        self.assertEqual(json_response["team_role_id"], self.admin_role.public_id)
        self.assertEqual(json_response["user_id"], self.test_user1.public_id)

    def test_team_memberships_post_success_for_multiple_teams(self):
        # First Teams Request
        response = self.send_team_memberships_post(
            self.test_team1.public_id,
            self.member_role.public_id,
            self.test_user1.public_id,
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json_response)
        self.assertEqual(json_response["team_id"], self.test_team1.public_id)
        self.assertEqual(json_response["team_role_id"], self.member_role.public_id)
        self.assertEqual(json_response["user_id"], self.test_user1.public_id)

        # Second Teams Request
        response = self.send_team_memberships_post(
            self.test_team2.public_id,
            self.member_role.public_id,
            self.test_user1.public_id,
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json_response)
        self.assertEqual(json_response["team_id"], self.test_team2.public_id)
        self.assertEqual(json_response["team_role_id"], self.member_role.public_id)
        self.assertEqual(json_response["user_id"], self.test_user1.public_id)

    def test_team_memberships_get(self):
        team_member1 = create_membership_in_db(
            self.test_team1, self.test_user1, self.member_role
        )
        team_member2 = create_membership_in_db(
            self.test_team1, self.test_user2, self.member_role
        )

        response = self.client.get(
            f"/teams/{self.test_team1.public_id}/memberships/", headers=self.headers
        )
        data = response.get_json()["data"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(item["id"] == team_member1.public_id for item in data))
        self.assertTrue(any(item["id"] == team_member2.public_id for item in data))

    def test_team_memberships_get_fails_with_invalid_team_id(self):
        team_id = "invalid-team-id"
        response = self.client.get(
            f"/teams/{team_id}/memberships/", headers=self.headers
        )

        json_response = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response["status"], "Failed")
        self.assertEqual(
            json_response["message"], f"The team with id {team_id} does not exist"
        )

    def send_team_memberships_post(self, team_id, role_id, user_id):
        team_member = {"user_id": user_id, "team_role_id": role_id}
        return self.client.post(
            f"/teams/{team_id}/memberships/", json=team_member, headers=self.headers
        )
