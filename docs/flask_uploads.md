# Flask-Uploads

For a good tutorial refer to http://www.patricksoftwareblog.com/tag/flask-uploads/

Allows to save files into server storage

To initialize, in the ```application.__init__```

```python
from flask_uploads import UploadSet, IMAGES, configure_uploads

images = UploadSet('images', IMAGES)

def create_app(config_name):
    ...
    configure_uploads(app, images)
```

Configurations to define
```python
UPLOADED_IMAGES_DEST = os.path.join(basedir, "application", "static", "img")
```

To save the file
```python
from application import images

saved_filename = images.save(filename)
```

# Problem with Flask-Uploads==0.2.1

This version is not compatible with ```werkzeug==1.0.1```
In ```venv/lib/python3.7/site-packages/flask_uploads.py```
you will have to change the way ```secure_filename``` and ```FileStorage``` are imported.

From
```python
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
```

To 
```python
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
```