from flask_testing import TestCase
from application import create_app, db
from application.auth.models import User


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app('test')
        return app

    def setUp(self):
        db.create_all()
        user = User(email="ad@min.com", username="admin", password="admin_user")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
