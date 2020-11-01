from flask import Blueprint

bsi_bp = Blueprint('bsi_bp', __name__, template_folder="templates")

from .views import *
from .sending_flight_views import *
from .tracking_status_views import *
from .represented_invididual_and_recipeints_views import *