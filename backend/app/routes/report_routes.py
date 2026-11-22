"""
MediScan AI - Report Upload, Management, and Download Routes
"""

import os
import uuid
from flask import Blueprint, request, jsonify, send_file, current_app
from werkzeug.utils import secure_filename
from app.models import db, Report
from app.utils.auth import login_required
from app.services.document_service import process_document, is_allowed_file
from app.services.pdf_generator import generate_report_pdf
from app.ml.classifier import classifier_service

report_bp = Blueprint('report_bp', __name__, url_prefix='/api/reports')

@report_bp.route('/upload', methods=['POST'])
@login_required
def upload_report(current_user):
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected."}), 400

    original_filename = file.filename
    if not is_allowed_file(original_filename):
        return jsonify({
            "success": False,
            "message": "Unsupported file format. Please upload a PDF, PNG, JPG, or JPEG file."
        }), 400

    # Safe filename generation
    base_name = secure_filename(original_filename)
    unique_id = uuid.uuid4().hex[:10]
    stored_filename = f"{unique_id}_{base_name}"

    upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'uploads'))
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, stored_filename)

    try:
        file.save(file_path)
        file_size = os.path.getsize(file_path)

        # Step 1: Document OCR & text extraction
        try:
            extracted_text = process_document(file_path, original_filename)
        except ValueError as val_err:
            # Insufficient text or invalid file
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({
                "success": False,
                "message": str(val_err)
            }), 422
        except Exception as doc_err:
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({
                "success": False,
                "message": f"Document processing failed: {str(doc_err)}"
            }), 500

        # Step 2: Machine Learning Classification
        try:
            ml_result = classifier_service.classify(extracted_text)
            predicted_category = ml_result["predicted_category"]
            confidence = ml_result["confidence_score"]
            all_probabilities = ml_result.get("all_probabilities", {})
        except Exception as ml_err:
            return jsonify({
                "success": False,
                "message": f"ML classification failed: {str(ml_err)}"
            }), 500

        # Step 3: Save Report to Database
        report = Report(
            user_id=current_user.id,
            filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type or 'application/octet-stream',
            extracted_text=extracted_text,
            predicted_category=predicted_category,
            confidence_score=confidence,
            processing_status='completed'
        )
        db.session.add(report)
        db.session.commit()

        report_dict = report.to_dict(include_full_text=True)
        report_dict["all_probabilities"] = all_probabilities

        return jsonify({
            "success": True,
            "message": f"Document successfully classified as '{predicted_category}' with {confidence*100:.1f}% confidence.",
            "report": report_dict
        }), 201

    except Exception as e:
        db.session.rollback()
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
        return jsonify({"success": False, "message": f"Upload failed: {str(e)}"}), 500

@report_bp.route('', methods=['GET'])
@login_required
def list_reports(current_user):
    query = Report.query.filter_by(user_id=current_user.id)

    # Search filter
    search_q = request.args.get('q', '').strip()
    if search_q:
        query = query.filter(
            db.or_(
                Report.filename.ilike(f'%{search_q}%'),
                Report.predicted_category.ilike(f'%{search_q}%'),
                Report.extracted_text.ilike(f'%{search_q}%')
            )
        )

    # Category filter
    category = request.args.get('category', '').strip()
    if category and category.lower() != 'all':
        query = query.filter(Report.predicted_category.ilike(category))

    # Sort
    sort_by = request.args.get('sort', 'newest')
    if sort_by == 'oldest':
        query = query.order_by(Report.uploaded_at.asc())
    elif sort_by == 'confidence_high':
        query = query.order_by(Report.confidence_score.desc())
    elif sort_by == 'confidence_low':
        query = query.order_by(Report.confidence_score.asc())
    else:  # newest
        query = query.order_by(Report.uploaded_at.desc())

    reports = query.all()
    return jsonify({
        "success": True,
        "count": len(reports),
        "reports": [r.to_dict(include_full_text=False) for r in reports]
    }), 200

@report_bp.route('/<int:report_id>', methods=['GET'])
@login_required
def get_report(current_user, report_id):
    report = Report.query.filter_by(id=report_id, user_id=current_user.id).first()
    if not report:
        return jsonify({"success": False, "message": "Report not found or unauthorized."}), 404

    return jsonify({
        "success": True,
        "report": report.to_dict(include_full_text=True)
    }), 200

@report_bp.route('/<int:report_id>', methods=['DELETE'])
@login_required
def delete_report(current_user, report_id):
    report = Report.query.filter_by(id=report_id, user_id=current_user.id).first()
    if not report:
        return jsonify({"success": False, "message": "Report not found or unauthorized."}), 404

    try:
        # Delete file from filesystem if present
        if report.file_path and os.path.exists(report.file_path):
            try:
                os.remove(report.file_path)
            except Exception:
                pass

        db.session.delete(report)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Report deleted successfully."
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Delete failed: {str(e)}"}), 500

@report_bp.route('/<int:report_id>/download', methods=['GET'])
@login_required
def download_report_pdf(current_user, report_id):
    report = Report.query.filter_by(id=report_id, user_id=current_user.id).first()
    if not report:
        return jsonify({"success": False, "message": "Report not found or unauthorized."}), 404

    try:
        pdf_stream = generate_report_pdf(report.to_dict(include_full_text=True), current_user.name)
        safe_name = f"MediScan_Report_{report.id}_{report.predicted_category.replace(' ', '_')}.pdf"
        return send_file(
            pdf_stream,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=safe_name
        )
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to generate PDF: {str(e)}"}), 500
