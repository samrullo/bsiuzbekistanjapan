import os

activate_this=os.path.abspath("venv/bin/activate")
with open(activate_thi) as file_:
    exec(file_.read(),dict(__file__=activate_this))

from application import create_app
application = create_app(os.environ.get('FLASK_ENV')