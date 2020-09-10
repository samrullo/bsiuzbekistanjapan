from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask import g, current_app
from flask import request
from flask_mail import Mail
from flask_login import LoginManager
import requests
from config import config
from .main import main_bp
import logging

bootstrap = Bootstrap()
babel = Babel()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])


    # set up logging
    if not app.debug:
        from logging import FileHandler, Formatter
        logging.basicConfig(level=logging.INFO)
        file_handler = FileHandler(app.config.get('LOG_FILE'))
        file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s %(lineno)s]'))
        app.logger.addHandler(file_handler)

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    app.logger.info(f"Finished initializations for db,bootstrap, moment, babel and mail and login_manager")

    with app.app_context():
        db.create_all()

        @babel.localeselector
        def get_locale():
            if g.current_lang:
                return g.current_lang
            else:
                g.current_lang = request.accept_languages.best_match(app.config.get('ALLOWED_LANGUAGES').keys())
                return g.current_lang

        from .auth import auth_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        return app
