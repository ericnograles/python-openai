import json
from functools import wraps
from jose import jwt
from jose.exceptions import JWTError
import requests
from flask import request, jsonify

def get_auth0_public_key():
    domain = "your-auth0-domain"  # Replace with your Auth0 domain
    url = f"https://{domain}/.well-known/jwks.json"
    response = requests.get(url)
    jwks = response.json()
    return jwks["keys"][0]

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "Authorization" not in request.headers:
            return jsonify({"message": "Missing Authorization header"}), 401

        auth_header = request.headers["Authorization"]
        parts = auth_header.split()

        if parts[0].lower() != "bearer":
            return jsonify({"message": "Invalid Authorization header"}), 401
        elif len(parts) == 1:
            return jsonify({"message": "Token not found"}), 401
        elif len(parts) > 2:
            return jsonify({"message": "Authorization header must be bearer token"}), 401

        token = parts[1]

        try:
            public_key = get_auth0_public_key()
            payload = jwt.decode(
                token,
                public_key,
                algorithms="RS256",
                options={"verify_signature": True, "verify_exp": True}
            )
            # Store the payload in Flask's global request object
            request.jwt_payload = payload
        except JWTError as e:
            return jsonify({"message": str(e)}), 401

        return f(*args, **kwargs)

    return decorated_function
