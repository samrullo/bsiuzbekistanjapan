import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BRAND_NAME = "BSI UZB-JP POST"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_SALT = os.environ.get('TOKEN_SALT')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_BTN_STYLE = 'dark'
    DEFAULT_LANG = "en"
    ALLOWED_LANGUAGES = {'en': 'English', 'uz': 'Uzbek'}
    LOG_FILE = "bsiuzbekistanjapan.log"

    SLOW_DB_QUERY_THRESHOLD = float(os.environ.get('SLOW_DB_QUERY_THRESHOLD'))

    # Gmail API related configurations
    GMAILAPI_CREDENTIALS_FILE = os.path.join(basedir, "credentials","bsiuzbekistanjapan_gmailapi.json")
    GMAILAPI_CREDENTIALS_FOLDER = os.path.join(basedir, "credentials")
    GMAILAPI_REDIRECT_URI = os.environ.get("GMAILAPI_REDIRECT_URI")

    GMAILAPI_SCOPES = [
        "https://www.googleapis.com/auth/gmail.compose",
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.labels",
        "https://www.googleapis.com/auth/gmail.modify",
        "email"
    ]

    # Google OAuth2 related configurations
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    # admins and moderators
    ADMINISTRATOR_EMAILS = os.environ.get("ADMINISTRATOR_EMAILS")
    MODERATOR_EMAILS = os.environ.get("MODERATOR_EMAILS")
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

    # configs for flask-upload
    UPLOADED_IMAGES_DEST = os.path.join(basedir, "application", "static", "img")
    UPLOADED_IMAGES_URL = "https://127.0.0.1/static/img/"

    # configs for uploading images to S3
    UPLOADED_PHOTOS_DEST = os.environ.get('UPLOADED_PHOTOS_DEST') or os.path.relpath("application/static/img")

    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    BUCKET_NAME = "elasticbeanstalk-ap-south-1-384482548730"
    BUCKET_URL = "https://elasticbeanstalk-ap-south-1-384482548730.s3.ap-south-1.amazonaws.com"
    BUCKET_FOLDER = "bsiuzbekistanjapanpost"

    TINIFY_API_KEY = os.environ.get('TINIFY_API_KEY')
    PHOTO_WIDTH = 500
    PHOTO_HEIGHT = 500

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
    MAIL_SERVER = os.environ.get("PROD_MAIL_SERVER")
    MAIL_PORT = os.environ.get("PROD_MAIL_PORT")
    # MAIL_USE_SSL = True
    MAIL_USE_TLS = True
    MAIL_SENDER = os.environ.get("PROD_MAIL_SENDER")
    MAIL_USERNAME = os.environ.get("PROD_MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("PROD_MAIL_PASSWORD")
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, "test.sqlite")


config = {'production': 'config.ProductionConfig',
          'development': 'config.DevelopmentConfig',
          'test': 'config.TestConfig'}
