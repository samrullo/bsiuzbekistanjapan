# I am getting "no such table " error even though I call db.create_all()

The reason is simple, you might be calling ```db.create_all()``` before registering your blueprint which imports
the model and uses it as in below example

```python
...

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    
    with app.app_context():
        
```