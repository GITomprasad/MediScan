"""
MediScan AI - Flask Application Factory
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from app.models import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Base configuration
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "mediscan.db")
    upload_path = os.path.join(base_dir, "uploads")
    os.makedirs(upload_path, exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'mediscan-super-secure-jwt-and-session-key-2026'),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=upload_path,
        MAX_CONTENT_LENGTH=12 * 1024 * 1024,  # 12MB limit
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=False  # Set True in production with HTTPS
    )

    if test_config:
        app.config.update(test_config)

    # Enable CORS
    CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"])

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.report_routes import report_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(dashboard_bp)

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "MediScan AI Backend API",
            "version": "1.0.0"
        }), 200

    # Ensure tables exist
    with app.app_context():
        db.create_all()

    return app
