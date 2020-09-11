from . import main_bp
from flask import render_template, redirect
from flask_babel import lazy_gettext as _
from application.utils.custom_url_for import url_for
from flask_login import login_required
from application.utils.permission_required import confirm_required
from flask import current_app
from flask import request, g


@main_bp.route('/')
def index():
    g.current_lang = current_app.config.get('DEFAULT_LANG')
    return redirect(url_for('main_bp.home'))


@main_bp.route('/switch_language/<switch_to_lang>')
def switch_language(switch_to_lang):
    g.current_lang = switch_to_lang
    return redirect(url_for(request.referrer))


@main_bp.route('/<lang>')
def home():
    return render_template('index.html', name="boss", page_header_title=_("Main page"))


@main_bp.route('/<lang>/secret')
@login_required
@confirm_required
def secret():
    return render_template("secret.html", page_header_title=_("Secret page"))


@main_bp.app_errorhandler(404)
def page_not_found(e):
    g.current_lang='en'
    return render_template("errors/error.html", page_header_title=_("Page not found")), 404


@main_bp.app_errorhandler(500)
def internal_server_error(e):
    g.current_lang='en'
    return render_template("errors/error.html", page_header_title=_("Internal server error")), 500
