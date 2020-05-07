from flask_login import current_user
from flask import abort
from functools import wraps
from .models import Permission

def permission_required(perm):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            if not current_user.can(perm):
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


