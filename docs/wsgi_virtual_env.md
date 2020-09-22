# Introduction
```mod_wsgi``` is required to make apache2 serve flask application responses.
You can follow https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/ for its installation.

# mod_wsgi with virtualenv

I ended up with below wsgi script

```python
import os
import sys

sys.path.insert(0,'/var/www/bsiuzbekistanjapan')

activate_this="/var/www/bsiuzbekistanjapan/venv/bin/activator.py"
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

env_vars=['FLASK_APP', 'FLASK_ENV', 'ADMIN_EMAIL',
           'DEV_MAIL_SERVER', 'DEV_MAIL_PORT', 'DEV_MAIL_USERNAME', 'DEV_MAIL_PASSWORD',
           'PROD_MAIL_SERVER', 'PROD_MAIL_PORT', 'PROD_MAIL_USERNAME', 'PROD_MAIL_PASSWORD',
           'SECRET_KEY', 'TOKEN_SALT', 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET', 'SLOW_DB_QUERY_THRESHOLD',
           'ADMIN_EMAIL', 'PROD_DATABASE_URI', 'DEV_DATABASE_URI']

def application(environ,start_response):
    for env_var in env_vars:
        os.environ[env_var]=environ[env_var]
    from bsiuzbekistanjapan import app as _application
    return _application(environ,start_response)
```

The only catch is that, ```activator.py``` wasn't under ```venv/bin``` by default.

I copied it from under ```virtualenv``` after installing it with pip.

```python
cp /var/www/bsiuzbekistanjapan/venv/lib/python3.6/site-packages/virtualenv/activation/activator.py ./venv/bin/
```