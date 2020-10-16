from flask import Blueprint

post_weight_bp = Blueprint("post_weight_bp", __name__, template_folder="templates")

from . import views
from . import recipient_views
from . import represented_individual_views
