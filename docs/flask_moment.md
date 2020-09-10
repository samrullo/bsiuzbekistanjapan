# Localization of date and times with Flask-Moment

The server needs uniform time units that are independant
of the location of each user, so typicalle Coordinated Universal
Time (UTC) is used

```python
$pip install Flask-Moment
```

```python
from flask_moment import Moment
moment=Moment(app)
```

```html
{% block scripts %}
{{super()}}
{{moment.include_moment()}}
{% endblock %}
```

