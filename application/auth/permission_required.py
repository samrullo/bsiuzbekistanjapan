from functools import wraps
from flask_login import current_user
from flask import abort
from flask import redirect
from application.utils.custom_url_for import url_for
from application.auth.permissions import Permissions

def confirm_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if not current_user.is_confirmed:
            return redirect(url_for('auth_bp.unconfirmed'))
        return func(*args, **kwargs)

    return decorator


def permission_required(perm):
    def decorator(func2):
        @wraps(func2)
        def decorated_function(*args, **kwargs):
            if not current_user.can(perm):
                abort(403)
            return func2(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(func):
    return permission_required(Permissions.ADMIN)(func)

def moderator_required(f):
    return permission_required(Permissions.ADD_BSI_WEIGHT)(f)