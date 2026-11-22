"""
MediScan AI - Authentication Routes
"""

from flask import Blueprint, request, jsonify, session
from app.models import db, User
from app.utils.auth import validate_email, validate_password, generate_token, login_required, get_current_user

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not name:
        return jsonify({"success": False, "message": "Full name is required."}), 400

    if not validate_email(email):
        return jsonify({"success": False, "message": "Please enter a valid email address."}), 400

    valid_pass, pass_err = validate_password(password)
    if not valid_pass:
        return jsonify({"success": False, "message": pass_err}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "An account with this email already exists."}), 409

    try:
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Establish session
        session['user_id'] = user.id
        session.permanent = True
        token = generate_token(user.id)

        return jsonify({
            "success": True,
            "message": "Registration successful! Welcome to MediScan AI.",
            "user": user.to_dict(),
            "token": token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Registration failed: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    session['user_id'] = user.id
    session.permanent = True
    token = generate_token(user.id)

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "user": user.to_dict(),
        "token": token
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    }), 200

@auth_bp.route('/me', methods=['GET'])
def get_me():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "message": "Not authenticated."}), 401

    return jsonify({
        "success": True,
        "user": user.to_dict()
    }), 200

@auth_bp.route('/password', methods=['PUT'])
@login_required
def change_password(current_user):
    data = request.get_json() or {}
    old_password = data.get('current_password', '')
    new_password = data.get('new_password', '')

    if not current_user.check_password(old_password):
        return jsonify({"success": False, "message": "Incorrect current password."}), 400

    valid_pass, pass_err = validate_password(new_password)
    if not valid_pass:
        return jsonify({"success": False, "message": pass_err}), 400

    try:
        current_user.set_password(new_password)
        db.session.commit()
        return jsonify({"success": True, "message": "Password changed successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Failed to update password: {str(e)}"}), 500
