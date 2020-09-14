
admin = Admin(app, url="/en/admin")
from application.admin_module.model_views import UserModelView
from application.auth.models import User
admin.add_view(UserModelView(User, db.session))

from application.admin_module.model_views import RoleModelView
from application.auth.models import Role
admin.add_view(RoleModelView(Role, db.session))
