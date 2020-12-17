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

# add ModelView to maintain PostWeight records
from .model_views import PostWeightView
from application.post_weight.models import PostWeight

admin_flsk.add_view(PostWeightView(PostWeight, db.session))

# add ModelView to maintain PostWeightContent records
from .model_views import PostWeightContentView
from application.post_weight.models import PostWeightContent

admin_flsk.add_view(PostWeightContentView(PostWeightContent, db.session))

# add ModelView to maintain BSIPostWeight
from .model_views import BSIPostWeightView
from application.bsi.models import BSIPostWeight

admin_flsk.add_view(BSIPostWeightView(BSIPostWeight, db.session))

# add ModelView to maintain UserPostWeightPrice
from .model_views import UserPostWeightPriceView
from application.post_weight.models import UserPostWeightPrice

admin_flsk.add_view(UserPostWeightPriceView(UserPostWeightPrice, db.session))
