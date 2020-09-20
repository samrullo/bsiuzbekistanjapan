from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_admin import Admin
from flask import g, session
from flask import request
from flask_mail import Mail
from flask_login import LoginManager
from config import config
import logging

bootstrap = Bootstrap()
babel = Babel()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
admin_flsk = Admin(name="bsiuzbekistanjapan")
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # set up logging
    if not app.debug:
        from logging import FileHandler, Formatter
        logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)s]')
        file_handler = FileHandler(app.config.get('LOG_FILE'))
        file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)s]'))
        app.logger.addHandler(file_handler)
    app.logger.info(f"Sender MAIL_USERNAME is {app.config.get('MAIL_USERNAME')}")

    db.init_app(app)
    admin_flsk.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    app.logger.info(f"Finished initializations for db,bootstrap, moment, babel and mail and login_manager")
    app.logger.info(f"SQLALCHEMY_DATABASE_URI is {app.config['SQLALCHEMY_DATABASE_URI']}")

    with app.app_context():
        db.create_all()

        @babel.localeselector
        def get_locale():
            if g.current_lang:
                return g.current_lang
            else:
                g.current_lang = request.accept_languages.best_match(app.config.get('ALLOWED_LANGUAGES').keys())
                return g.current_lang

        from .main import main_bp
        from .auth import auth_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)

        # add post_weight blueprint
        from .post_weight import post_weight_bp
        app.register_blueprint(post_weight_bp)

        # add bsi blueprint
        from .bsi import bsi_bp
        app.register_blueprint(bsi_bp)

        # add admin blueprint
        from application.admin import admin_bp
        app.register_blueprint(admin_bp)

        from application.auth.models import Role
        Role.insert_roles()
        return app
