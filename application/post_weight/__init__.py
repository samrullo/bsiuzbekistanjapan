from flask import Blueprint

post_weight_bp = Blueprint("post_weight_bp", __name__, template_folder="templates")

import application.post_weight.views