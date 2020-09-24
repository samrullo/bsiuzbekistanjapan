# Flask-Babel

## Installation

```
$ pip install Flask-Babel
```

## How to do it

myapp/__init__.py
```python
from flask_babel import Babel

ALLOWED_LANGUAGES={"en":"English","uz":"Uzbek","ru":"Russian"}

babel=Babel(app)
```

babel.cfg
```
[python : catalog/**.py]
[jinja2: templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```

application/__init__.py
```python
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(ALLOWED_LANGUAGES.keys())
```

home.html
```html
{% block content %}
<h1>{{_('Welcome to the site')}}</h1>
{% endblock %}
```

_ is shortcut to babel gettext.

- Next run pybabel extract to generate messages.pot file. 
This file will have all the messages scheduled for translation 
```
$pybabel extract -F my_app/babel.cfg -o my_app/messages.pot my_app/
```

- Next run pybabel init, to generate messages.po file, in which we will input translation
If you are using application factor, then better to specify output folder 
as application/translations
```
$pybabel init -i my_app/messages.pot -d my_app/application/translations -l uz
```
manually editing messages.po will look like below
```
#: my_app/templates/home.html:6
msgid "Welcome to the site"
msgstr "Sitega xush kelibsiz"
```

- Finally run pybabel compile
```
$pybabel compile -d my_app/application/translations
```