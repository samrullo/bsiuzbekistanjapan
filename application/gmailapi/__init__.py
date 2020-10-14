from flask import Blueprint

gmailapi_bp = Blueprint('gmailapi_bp', __name__, template_folder='templates')
from . import views
