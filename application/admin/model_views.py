from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()


class RoleModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()
