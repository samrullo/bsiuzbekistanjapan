import unittest
from base_test_class import BaseTestCase
from application.auth.models import User
from application.auth.forms import RegisterForm
from flask import current_app, g
from application import db
from wtforms import ValidationError


class RegisterFormTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        user = User(email="test@test.com", name="testuser")
        self.app.config['WTF_CSRF_ENABLED'] = False
        g.current_lang = "en"

    def test_validate_success_register_form(self):
        form = RegisterForm(email="nohbus.veollurma@gmail.com", name="my name", password="mysecret",
                            confirm_password="mysecret")
        self.assertTrue(form.validate())

    def test_confirm_password(self):
        form = RegisterForm(email="nohbus.veollurma@gmail.com", name="my name", password="mysecret",
                            confirm_password="wrongsecret")
        self.assertFalse(form.validate())

    def test_email_format(self):
        form = RegisterForm(email="nohbus.veollurmagmail.com", name="my name", password="mysecret",
                            confirm_password="mysecret")
        self.assertFalse(form.validate())

    def test_email_exists(self):
        user = User(email="nohbus.veollurma@gmail.com", name="nohbus")
        db.session.add(user)
        db.session.commit()
        form = RegisterForm(email="nohbus.veollurma@gmail.com", name="my name", password="mysecret",
                            confirm_password="mysecret")
        with self.assertRaises(ValidationError) as e:
            form.validate_email(form.email)
            self.assertTrue("Email already exists" in e.exception)


if __name__ == "__main__":
    unittest.main()
