import os
import unittest

from flask import current_app
from flask_testing import TestCase

from app import create_app
from app.config import basedir


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        return create_app('dev')

    def test_app_is_development(self):
        self.assertFalse(self.app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    def create_app(self):
        return create_app('test')

    def test_app_is_testing(self):
        self.assertFalse(self.app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(self.app.config['DEBUG'])


class TestProductionConfig(TestCase):
    def create_app(self):
        return create_app('prod')

    def test_app_is_production(self):
        self.assertTrue(self.app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
