from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import current_app


class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_confirmed and current_user.is_administrator()


class RoleModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_confirmed and current_user.is_administrator()
