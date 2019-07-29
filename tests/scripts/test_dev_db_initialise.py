from flask_testing import TestCase
from flask_migrate import upgrade, downgrade
from app import db, create_app
from scripts import dev_db_initialise
from app.users.model import User
from app.teams.model import Team
from app.team_memberships.model import Membership


class TestDevDbInitialise(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        db.drop_all()
        upgrade(x_arg='data=true')

    def tearDown(self):
        db.session.remove()
        downgrade(x_arg='data=true', revision='base')

    def test_initialise(self):
        dev_db_initialise.initialise()
        self.assertEqual(User.query.count(), 2)
        self.assertEqual(Team.query.count(), 1)
        self.assertEqual(Membership.query.count(), 2)
