from . import main_bp
from flask import render_template, redirect
from flask import url_for as flask_url_for
from flask_babel import lazy_gettext as _
from application.utils.custom_url_for import url_for
from flask_login import login_required
from application.auth.permission_required import confirm_required
from flask import current_app
from flask import request, g
from flask_sqlalchemy import get_debug_queries
from flask_login import current_user


@main_bp.app_context_processor
def inject_url_for():
    return {'url_for': lambda endpoint, **kwargs: flask_url_for(endpoint, lang=g.current_lang, **kwargs)}


@main_bp.app_context_processor
def inject_number_formatter():
    def format_number(amount):
        return "{:,.2f}".format(amount)

    return dict(format_number=format_number)


@main_bp.before_app_request
def before():
    if request.view_args and 'lang' in request.view_args:
        selected_lang_value = request.view_args['lang']
        if selected_lang_value in current_app.config.get('ALLOWED_LANGUAGES'):
            g.current_lang = request.view_args['lang']
        else:
            g.current_lang = 'en'
        request.view_args.pop('lang')
    if 'lc' in request.args:
        g.current_lang = request.args.get('lc')


@main_bp.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['SLOW_DB_QUERY_THRESHOLD']:
            current_app.logger.warning('Slow query : %s\nParameters: %s\nDuration: %f\nContext:%s\n' %
                                       (query.statement, query.parameters, query.duration, query.context))
    return response


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
    if current_user.is_authenticated and not current_user.is_confirmed:
        return redirect(url_for('auth_bp.unconfirmed'))
    return render_template('index.html', page_header_title=_("BSI Delivery services"))


@main_bp.route('/<lang>/secret')
@login_required
@confirm_required
def secret():
    return render_template("secret.html", page_header_title=_("Secret page"))


@main_bp.route('/<lang>/aboutus')
def aboutus():
    return render_template("about_us.html", page_header_title=_("About us"))


@main_bp.app_errorhandler(404)
def page_not_found(e):
    g.current_lang = 'en'
    return render_template("errors/error.html", page_header_title=_("Page not found")), 404


@main_bp.app_errorhandler(500)
def internal_server_error(e):
    g.current_lang = 'en'
    return render_template("errors/error.html", page_header_title=_("Internal server error")), 500

@main_bp.route("/<lang>/test/<name>")
def test(name):
    current_app.logger.info(f"request endpoint is {request.endpoint}")
    return render_template("test.html",name=name)