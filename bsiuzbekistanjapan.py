import os
from application import create_app, db
from application.auth.models import User, Role, Permissions
from application.bsi.models import BSIPostWeight
from application.main.models import BusinessGlobalVariable
from flask_migrate import Migrate
from flask import g, request, current_app
from flask import url_for as flask_url_for

app = create_app(os.environ['FLASK_ENV'])

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, BSIPostWeight=BSIPostWeight, Role=Role, app=app, Permissions=Permissions,
                BusinessGlobalVariable=BusinessGlobalVariable)


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


if __name__ == "__main__":
    app.run()
