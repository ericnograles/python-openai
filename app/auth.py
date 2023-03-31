from functools import wraps
from flask import request, jsonify
import jwt
from .models import User

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Missing token"}), 401

        try:
            # Validate the JWT and extract the Auth0 ID
            payload = jwt.decode(token, 'YOUR_AUTH0_PUBLIC_KEY', algorithms=['RS256'])
            auth0_id = payload['sub']

            # Look up the User in the database using the Auth0 ID
            user = User.query.filter_by(auth0_id=auth0_id).first()

            if not user:
                return jsonify({"error": "User not found"}), 404

            # Attach the user to the request
            request.user = user

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return wrapper

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Get the user from your authentication middleware.
            # You should have the user information available in the request context.
            user = request.user

            # Check if the user role is in the allowed roles.
            if user.role.name not in allowed_roles:
                return jsonify({"error": "Unauthorized access"}), 403

            return f(*args, **kwargs)

        return wrapper

    return decorator
