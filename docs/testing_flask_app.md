# Testing Flask application

## Flask-Testing
Flask-Testing allows to test flask application more easily.
It comes with ```client``` variable that allows to send GET request to routes and return response.

Let's say we want to test a simple ```home``` route

```python
from flask_testing import TestCase

class MyTestCase(TestCase):
    def create_app(self):
        app=create_app()
        return app
    
    def setUp(self)->None:
        super().setUp()
        self.app=self.create_app()
        self.app_context=self.app.app_context()
        self.app.context.push()
        self.app.config['WTF_CSRF_ENABLED']=False
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        self.app_context.pop()
        super().tearDown()
    
    def test_home(self):
        response=self.client.get("/", follow_redirects=True)
        self.assertTrue(response.status_code==200)
```

To test functions that utilize ```flask.session```

```python
def test_set_form_data_into_session(self):
    with self.app.test_request_context():
        from flask import session
        form=SomeForm()
        set_form_data_into_session(form)
        self.assertEqual(session['some_key'],form.some_key.data)
```

To test views that utilize forms, you have to make sure that you have set
```SECRET_KEY```

```python
class MyTestCase(TestCase):
    def create_app(self):
        app=create_app()
        return app
    
    def setUp(self)->None:
        super().setUp()
        self.app=self.create_app()
        self.app_context=self.app.app_context()
        self.app.context.push()
        self.app.config['SECRET_KEY']="mysecretkey"
        db.create_all()
    
    def test_some_view_that_uses_form(self):
        with self.app.test_client() as c:
            response=c.get("/some_route",follow_redirects=True)
            self.assertEqual(response.status_code,200)

```