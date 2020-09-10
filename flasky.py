from application import create_app, db
from application.auth.models import User, Role
from flask_migrate import Migrate
from flask import g, request, current_app
from flask import url_for as flask_url_for

app = create_app('development')

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, app=app)


@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command('create_db')
def create_db():
    db.create_all()


@app.cli.command('drop_db')
def drop_db():
    db.drop_all()


@app.before_request
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


@app.context_processor
def inject_url_for():
    return {'url_for': lambda endpoint, **kwargs: flask_url_for(endpoint, lang=g.current_lang, **kwargs)}
