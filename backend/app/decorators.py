from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify
from app.models import User

def roles_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or role not in [r.name for r in user.roles]:
                return jsonify({"msg": "Permission denied"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
