import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BRAND_NAME="BSI UZB-JP POST"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_SALT = os.environ.get('TOKEN_SALT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_BTN_STYLE = 'dark'
    DEFAULT_LANG="en"
    ALLOWED_LANGUAGES = {'en': 'English', 'uz': 'Uzbek'}
    LOG_FILE = "bsiuzbekistanjapan.log"

    # Google OAuth2 related configurations
    GOOGLE_CLIENT_ID=os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET=os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    @staticmethod
    def init_app():
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = os.environ.get("DEV_MAIL_SERVER")
    MAIL_PORT = os.environ.get("DEV_MAIL_PORT")
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("DEV_MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("DEV_MAIL_PASSWORD")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, "dev.sqlite")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, "prod.sqlite")


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, "test.sqlite")


config = {'production': 'config.ProductionConfig',
          'development': 'config.DevelopmentConfig',
          'test': 'config.TestConfig'}
