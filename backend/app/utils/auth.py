"""
MediScan AI - Authentication & Security Utilities
Handles session verification, token generation/decoding, password validation, and route decorators.
"""

import re
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import session, request, jsonify, current_app
import jwt
from app.models import db, User

JWT_SECRET_FALLBACK = "mediscan-super-secure-jwt-secret-key-32-bytes-long-for-hmac-sha256!"

def validate_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email.strip()))

def validate_password(password: str) -> tuple[bool, str]:
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isupper() for c in password) and not any(c.isdigit() for c in password):
        return False, "Password should contain at least one uppercase letter or number."
    return True, ""

def generate_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'user_id': user_id,
        'exp': now + timedelta(days=7),
        'iat': now
    }
    secret = current_app.config.get('SECRET_KEY', JWT_SECRET_FALLBACK)
    if len(secret) < 32:
        secret = JWT_SECRET_FALLBACK
    return jwt.encode(payload, secret, algorithm='HS256')

def get_current_user():
    """Retrieve authenticated user from Session or Authorization Header."""
    user_id = session.get('user_id')
    
    # Check Authorization header if not found in session
    if not user_id:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1].strip()
            secret = current_app.config.get('SECRET_KEY', JWT_SECRET_FALLBACK)
            if len(secret) < 32:
                secret = JWT_SECRET_FALLBACK
            try:
                payload = jwt.decode(token, secret, algorithms=['HS256'])
                user_id = payload.get('user_id')
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                return None

    if user_id:
        return db.session.get(User, user_id)
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({
                "success": False,
                "message": "Authentication required. Please log in to access this resource."
            }), 401
        return f(user, *args, **kwargs)
    return decorated_function
