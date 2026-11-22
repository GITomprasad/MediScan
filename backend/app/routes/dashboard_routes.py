"""
MediScan AI - Dashboard & Analytics Routes
Computes real-time statistics, category distribution, monthly trends, and model metrics.
"""

import json
import os
from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from sqlalchemy import func
from app.models import db, Report
from app.utils.auth import login_required

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/api')

CATEGORIES = ["Blood Test", "Diabetes", "Cardiology", "Radiology", "Kidney", "Liver"]

@dashboard_bp.route('/dashboard/stats', methods=['GET'])
@login_required
def get_dashboard_stats(current_user):
    user_id = current_user.id
    total_reports = Report.query.filter_by(user_id=user_id).count()

    # Counts per category
    category_counts = {}
    rows = (
        db.session.query(Report.predicted_category, func.count(Report.id))
        .filter_by(user_id=user_id)
        .group_by(Report.predicted_category)
        .all()
    )
    for cat, count in rows:
        category_counts[cat] = count

    blood_test_count = category_counts.get("Blood Test", 0)
    radiology_count = category_counts.get("Radiology", 0)
    cardiology_count = category_counts.get("Cardiology", 0)
    diabetes_count = category_counts.get("Diabetes", 0)
    kidney_count = category_counts.get("Kidney", 0)
    liver_count = category_counts.get("Liver", 0)

    other_count = diabetes_count + kidney_count + liver_count

    # Average confidence
    avg_conf = (
        db.session.query(func.avg(Report.confidence_score))
        .filter_by(user_id=user_id)
        .scalar()
    ) or 0.0

    # Latest report
    latest_report = (
        Report.query.filter_by(user_id=user_id)
        .order_by(Report.uploaded_at.desc())
        .first()
    )

    return jsonify({
        "success": True,
        "stats": {
            "total_reports": total_reports,
            "blood_test_count": blood_test_count,
            "radiology_count": radiology_count,
            "cardiology_count": cardiology_count,
            "diabetes_count": diabetes_count,
            "kidney_count": kidney_count,
            "liver_count": liver_count,
            "other_count": other_count,
            "average_confidence": round(float(avg_conf), 4),
            "latest_upload": latest_report.uploaded_at.isoformat() if latest_report else None
        }
    }), 200

@dashboard_bp.route('/dashboard/recent', methods=['GET'])
@login_required
def get_recent_reports(current_user):
    recent = (
        Report.query.filter_by(user_id=current_user.id)
        .order_by(Report.uploaded_at.desc())
        .limit(5)
        .all()
    )
    return jsonify({
        "success": True,
        "reports": [r.to_dict(include_full_text=False) for r in recent]
    }), 200

@dashboard_bp.route('/analytics/categories', methods=['GET'])
@login_required
def get_category_analytics(current_user):
    user_id = current_user.id
    total = Report.query.filter_by(user_id=user_id).count()

    rows = (
        db.session.query(Report.predicted_category, func.count(Report.id))
        .filter_by(user_id=user_id)
        .group_by(Report.predicted_category)
        .all()
    )
    cat_map = {r[0]: r[1] for r in rows}

    distribution = []
    category_colors = {
        "Blood Test": "#ef4444",
        "Diabetes": "#f59e0b",
        "Cardiology": "#ec4899",
        "Radiology": "#8b5cf6",
        "Kidney": "#06b6d4",
        "Liver": "#10b981"
    }

    for cat in CATEGORIES:
        count = cat_map.get(cat, 0)
        percentage = round((count / total * 100), 1) if total > 0 else 0
        distribution.append({
            "category": cat,
            "count": count,
            "percentage": percentage,
            "color": category_colors.get(cat, "#3b82f6")
        })

    return jsonify({
        "success": True,
        "total": total,
        "distribution": distribution
    }), 200

@dashboard_bp.route('/analytics/monthly', methods=['GET'])
@login_required
def get_monthly_analytics(current_user):
    user_id = current_user.id
    now = datetime.utcnow()

    # Generate last 6 months list
    months_data = []
    for i in range(5, -1, -1):
        target_date = now - timedelta(days=i * 30)
        month_label = target_date.strftime('%b %Y')
        year = target_date.year
        month = target_date.month

        # Count reports in this month
        count = (
            db.session.query(func.count(Report.id))
            .filter(Report.user_id == user_id)
            .filter(func.strftime('%Y', Report.uploaded_at) == str(year))
            .filter(func.strftime('%m', Report.uploaded_at) == f"{month:02d}")
            .scalar()
        ) or 0

        months_data.append({
            "month": month_label,
            "uploads": count
        })

    return jsonify({
        "success": True,
        "monthly": months_data
    }), 200

@dashboard_bp.route('/analytics/model-metrics', methods=['GET'])
def get_model_metrics():
    """Return actual ML training metrics and test-set performance."""
    metrics_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "trained_models",
        "model_metrics.json"
    )
    if os.path.exists(metrics_path):
        with open(metrics_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify({"success": True, "metrics": data}), 200
    return jsonify({
        "success": False,
        "message": "Model metrics file not found. Train the model first."
    }), 404
