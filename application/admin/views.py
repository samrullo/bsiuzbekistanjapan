from application import db,admin_flsk

from application.admin.model_views import UserModelView
from application.auth.models import User
admin_flsk.add_view(UserModelView(User, db.session))

from application.admin.model_views import RoleModelView
from application.auth.models import Role
admin_flsk.add_view(RoleModelView(Role, db.session))
