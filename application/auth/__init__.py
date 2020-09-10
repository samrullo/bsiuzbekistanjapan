from flask import Blueprint

auth_bp=Blueprint('auth_bp',__name__,template_folder="templates")

import application.auth.views
import application.auth.views_google_login