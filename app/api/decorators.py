from functools import wraps
from flask import g
from .errors import forbidden


def permission_required(permission):
    def wrapper(func):
        @wraps(func)
        def decorator(*args,**kwargs):
            user=g.current_user
            if not user.can(permission):
                return forbidden('Insufficient permissions')
            return func(*args,**kwargs)
        return decorator
    return wrapper
