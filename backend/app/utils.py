from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify
from app.models import User

def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return jsonify({"msg": "User not found"}), 404
            user_roles = [role.name for role in user.roles]
            if not any(role in user_roles for role in roles):
                return jsonify({"msg": "Insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
