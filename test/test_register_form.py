import unittest
from base_test_class import BaseTestCase
from application.auth.models import User
from application.auth.forms import RegisterForm
from flask import current_app,g
from application import db


class RegisterFormTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        user = User(email="test@test.com", username="testuser")
        self.app.config['WTF_CSRF_ENABLED']=False
        g.current_lang="en"

    def test_validate_success_register_form(self):
        form = RegisterForm(email="nohbus.veollurma@gmail.com", username="myusername", password="mysecret", confirm_password="mysecret")
        self.assertTrue(form.validate())

    def test_confirm_password(self):
        form=RegisterForm(email="nohbus.veollurma@gmail.com", username="myusername", password="mysecret", confirm_password="wrongsecret")
        self.assertFalse(form.validate())

    def test_email_format(self):
        form = RegisterForm(email="nohbus.veollurmagmail.com", username="myusername", password="mysecret",
                            confirm_password="mysecret")
        self.assertFalse(form.validate())

    def test_email_exists(self):
        user=User(email="nohbus.veollurma@gmail.com",username="nohbus")
        db.session.add(user)
        db.session.commit()
        form = RegisterForm(email="nohbus.veollurma@gmail.com", username="myusername", password="mysecret",
                            confirm_password="mysecret")
        self.assertFalse(form.validate())
        self.assertFalse(form.validate_email(form.email))

if __name__=="__main__":
    unittest.main()