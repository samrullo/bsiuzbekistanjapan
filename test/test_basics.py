import unittest
from flask import current_app
from application import create_app,db
from base_test_class import BaseTestCase

class BasicsTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.app=create_app('test')
        self.app_context=self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_config_is_set_to_test(self):
        self.assertTrue(current_app.config['TESTING'])