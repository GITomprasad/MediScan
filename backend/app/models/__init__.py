"""
MediScan AI - Database Models & Base Configuration
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def get_utc_now():
    return datetime.now(timezone.utc)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=get_utc_now)

    reports = db.relationship('Report', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "total_reports": len(self.reports)
        }

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_size = db.Column(db.Integer, default=0)
    mime_type = db.Column(db.String(64), default='application/octet-stream')
    extracted_text = db.Column(db.Text, nullable=False)
    predicted_category = db.Column(db.String(64), nullable=False, index=True)
    confidence_score = db.Column(db.Float, default=0.0)
    processing_status = db.Column(db.String(32), default='completed')
    uploaded_at = db.Column(db.DateTime, default=get_utc_now, index=True)

    def to_dict(self, include_full_text: bool = True):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "extracted_text": self.extracted_text if include_full_text else (self.extracted_text[:300] + '...' if len(self.extracted_text) > 300 else self.extracted_text),
            "predicted_category": self.predicted_category,
            "confidence_score": round(float(self.confidence_score or 0.0), 4),
            "processing_status": self.processing_status,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }
