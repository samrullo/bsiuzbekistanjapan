import unittest
from application.auth.models import User, Role
from application import create_app, db
from base_test_class import BaseTestCase


class UserModelTestCase(BaseTestCase):
    def test_direct_password_access(self):
        u = User(password="secret")
        with self.assertRaises(AttributeError):
            u.password

    def test_password_setter(self):
        u = User(password="secret")
        self.assertTrue(u.password_hash is not None)

    def test_password_verification(self):
        u = User(password="secret")
        self.assertTrue(u.verify_password("secret"))
        self.assertFalse(u.verify_password("wrong-secret"))

    def test_password_salts_random(self):
        u1 = User(password="secret")
        u2 = User(password="secret")
        self.assertTrue(u1.password_hash != u2.password_hash)
