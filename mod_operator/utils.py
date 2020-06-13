from flask import abort,session
from functools import wraps

def operator_only_view(func):
    @wraps(func)
    def decorator(*args,**kwargs):
        if session.get('Op_id') is None:
            abort(401)
        if session.get('role') != 3:
            abort(403)
        return func(*args,**kwargs)
    return decorator