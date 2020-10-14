## How to implement unauthorized access callback

```python
from application import login_manager

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth_bp.login',next=request.path))
```