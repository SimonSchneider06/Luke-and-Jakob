from functools import wraps 
from flask import abort 
from flask_login import current_user
from .models import Role


def admin_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            
            admin_role = Role.get_role_by_name("Admin")
            if current_user.role_id != admin_role.id:
                abort(403)
            return f(*args, **kwargs)

        return decorated_function 
    return decorator