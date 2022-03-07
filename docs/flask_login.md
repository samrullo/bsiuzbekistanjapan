## How to implement unauthorized access callback

```python
from application import login_manager


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth_bp.login', next=request.path))
```

## How flask_login LoginManager works

As the <a href="https://flask-login.readthedocs.io/en/latest/">documentation</a> mentions Flask-Login by default uses
sessions to authenticate users. What this means is that it looks for a ```user_id``` key in session and then try load
the user based on that user_id. This in turn means you have to provide ```user_loader``` as below example

```python
from flask_login import login_manager
from models import User


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
```

## How to authorize test_client

When testing requests to routes that require the user to be logged in You can authorize your test client as below

```python
class MyTestCase(TestCase):
    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client(use_cookies=True)
        with self.client as c:
            c.post("/login", data={"username": "the_user", "password": "secret"})
```
