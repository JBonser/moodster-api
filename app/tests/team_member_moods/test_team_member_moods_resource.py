from flask_testing import TestCase
from flask_migrate import upgrade, downgrade
from app import create_app, db
from app.teams.service import create_team_in_db
from app.users.service import create_user_in_db
from app.team_members.service import create_team_member_in_db
from app.mood_templates.service import create_mood_template_in_db
from app.moods.service import create_mood_in_db
from app.team_roles.service import get_team_role_by_name
from app.team_member_moods.service import create_team_member_mood_in_db


class TestTeamMembersMoodsResource(TestCase):
    def create_app(self):
        return create_app("test")

    def setUp(self):
        upgrade(x_arg="data=true")
        self.mood_template = create_mood_template_in_db("test_template")
        self.mood1 = create_mood_in_db("mood1", "#ffffff", self.mood_template)
        self.mood2 = create_mood_in_db("mood2", "#aaaaaa", self.mood_template)
        self.test_team1 = create_team_in_db("test_team_name")
        self.test_team2 = create_team_in_db("test_team_name2")
        self.test_user1 = create_user_in_db("test_user1@test.com", "password")
        self.test_user2 = create_user_in_db("test_user2@test.com", "password")
        self.member_role = get_team_role_by_name("Member")
        self.test_team_member_1 = create_team_member_in_db(
            self.test_team1, self.test_user1, self.member_role
        )
        self.test_team_member_2 = create_team_member_in_db(
            self.test_team1, self.test_user2, self.member_role
        )

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg="data=true", revision="base")

    def test_submit_team_member_mood_success(self):
        response = self.client.post(
            f"/teams/{self.test_team1.public_id}"
            f"/members/{self.test_team_member_1.public_id}/moods",
            json={"mood_id": self.mood1.public_id},
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", json_response)
        self.assertEqual(
            json_response["team_member_id"], self.test_team_member_1.public_id
        )
        self.assertEqual(json_response["mood_id"], self.mood1.public_id)

    def test_submit_team_member_mood_fails_with_invalid_team(self):
        invalid_id = 'invalid_team_id'
        response = self.client.post(
            f"/teams/{invalid_id}/members/{self.test_team_member_1.public_id}/moods",
            json={"mood_id": self.mood1.public_id},
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response["status"], "Failed")
        self.assertEqual(
            json_response["message"], f"Team with id {invalid_id} does not exist"
        )

    def test_submit_team_member_mood_fails_with_invalid_mood(self):
        invalid_id = "invalid_mood_id"
        response = self.client.post(
            f"/teams/{self.test_team1.public_id}"
            f"/members/{self.test_team_member_1.public_id}/moods",
            json={"mood_id": invalid_id},
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response["status"], "Failed")
        self.assertEqual(
            json_response["message"], f"Mood with id {invalid_id} does not exist"
        )

    def test_submit_team_member_mood_fails_with_invalid_team_member(self):
        invalid_id = "invalid_team_member_id"
        response = self.client.post(
            f"/teams/{self.test_team1.public_id}/members/{invalid_id}/moods",
            json={"mood_id": self.mood1.public_id},
        )

        json_response = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_response["status"], "Failed")
        self.assertEqual(
            json_response["message"],
            f"Team Member with id {invalid_id} does not exist",
        )

    def test_team_mood_get(self):
        set_mood_1 = create_team_member_mood_in_db(self.test_team_member_1, self.mood1)
        set_mood_2 = create_team_member_mood_in_db(self.test_team_member_1, self.mood2)
        set_mood_3 = create_team_member_mood_in_db(self.test_team_member_2, self.mood1)
        set_mood_4 = create_team_member_mood_in_db(self.test_team_member_2, self.mood2)
        response = self.client.get(f"/teams/{self.test_team1.public_id}/moods")
        data = response.get_json()["data"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            any(
                item["team_member_id"] == self.test_team_member_1.public_id
                or item["team_member_id"] == self.test_team_member_2.public_id
                for item in data
            )
        )
        self.assertTrue(
            any(
                item["mood_id"] == self.mood1.public_id
                or item["mood_id"] == self.mood2.public_id
                for item in data
            )
        )
        self.assertTrue(
            any(
                item["id"] == set_mood_1.public_id
                or item["id"] == set_mood_2.public_id
                or item["id"] == set_mood_3.public_id
                or item["id"] == set_mood_4.public_id
                for item in data
            )
        )

    def test_team_member_mood_get(self):
        set_mood_1 = create_team_member_mood_in_db(self.test_team_member_1, self.mood1)
        set_mood_2 = create_team_member_mood_in_db(self.test_team_member_1, self.mood2)
        set_mood_3 = create_team_member_mood_in_db(self.test_team_member_1, self.mood1)
        set_mood_4 = create_team_member_mood_in_db(self.test_team_member_1, self.mood2)
        response = self.client.get(
            f"/teams/{self.test_team1.public_id}/"
            f"members/{self.test_team_member_1.public_id}/moods"
        )
        json_response = response.get_json()
        data = json_response["data"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            any(
                item["team_member_id"] == self.test_team_member_1.public_id
                for item in data
            )
        )
        self.assertTrue(
            any(
                item["mood_id"] == self.mood1.public_id
                or item["mood_id"] == self.mood2.public_id
                for item in data
            )
        )
        self.assertTrue(
            any(
                item["id"] == set_mood_1.public_id
                or item["id"] == set_mood_2.public_id
                or item["id"] == set_mood_3.public_id
                or item["id"] == set_mood_4.public_id
                for item in data
            )
        )
