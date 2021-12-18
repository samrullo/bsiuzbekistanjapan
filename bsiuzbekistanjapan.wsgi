import os
import sys

sys.path.insert(0,'/var/www/bsiuzbekistanjapan')

activate_this="/var/www/bsiuzbekistanjapan/venv/bin/activator.py"
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

env_vars =  ['FLASK_APP', 'FLASK_ENV', 'ADMIN_EMAIL', 'DEV_MAIL_SERVER', 'DEV_MAIL_PORT', 'DEV_MAIL_USERNAME', 'DEV_MAIL_PASSWORD', 'PROD_MAIL_SERVER', 'PROD_MAIL_PORT', 'PROD_MAIL_SENDER', 'PROD_MAIL_USERNAME', 'PROD_MAIL_PASSWORD', 'SECRET_KEY', 'TOKEN_SALT', 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'GMAILAPI_REDIRECT_URI', 'PROD_DATABASE_URI', 'DEV_DATABASE_URI', 'SLOW_DB_QUERY_THRESHOLD', 'AWS_ACCESS_KEY', 'AWS_SECRET_ACCESS_KEY', 'TINIFY_API_KEY', 'PROD_MAIL_USERNAME', 'PROD_MAIL_SENDER', 'PROD_MAIL_PASSWORD']


def application(environ,start_response):
    for env_var in env_vars:
        os.environ[env_var]=environ[env_var]
    from bsiuzbekistanjapan import app as _application
    return _application(environ,start_response)