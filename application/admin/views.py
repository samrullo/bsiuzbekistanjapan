from application import db, admin_flsk

from application.admin.model_views import UserModelView
from application.auth.models import User

admin_flsk.add_view(UserModelView(User, db.session))

from application.admin.model_views import RoleModelView
from application.auth.models import Role

admin_flsk.add_view(RoleModelView(Role, db.session))

from application.admin.model_views import CountryModelView
from application.post_weight.models import Country

admin_flsk.add_view(CountryModelView(Country, db.session))

from .model_views import RepresentedIndividualView
from application.post_weight.models import RepresentedIndividual

admin_flsk.add_view(RepresentedIndividualView(RepresentedIndividual, db.session))

from .model_views import RecipientView
from application.post_weight.models import Recipient

admin_flsk.add_view(RecipientView(Recipient, db.session))
