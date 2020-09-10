from functools import wraps
from flask_login import current_user
from flask import redirect
from application.utils.custom_url_for import url_for

def confirm_required(func):
    @wraps(func)
    def decorator(*args,**kwargs):
        if not current_user.is_confirmed:
            return redirect(url_for('auth_bp.unconfirmed'))
        return func(*args,**kwargs)
    return decorator