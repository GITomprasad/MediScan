"""
MediScan AI - End-to-End Test Suite
Tests all 18 requirements:
1. User registration
2. User login
3. Invalid login
4. PDF upload
5. Image upload
6. OCR text extraction
7. Blood Test classification
8. Diabetes classification
9. Cardiology classification
10. Radiology classification
11. Kidney classification
12. Liver classification
13. Empty document handling
14. Invalid file handling
15. Report history
16. Report deletion
17. PDF result download
18. Unauthorized access prevention
"""

import io
import os
import pytest
from PIL import Image, ImageDraw, ImageFont
import fitz  # PyMuPDF
from app import create_app
from app.models import db, User, Report

@pytest.fixture(scope="module")
def app_instance():
    test_db = os.path.join(os.path.dirname(__file__), "test_mediscan.db")
    upload_dir = os.path.join(os.path.dirname(__file__), "test_uploads")
    os.makedirs(upload_dir, exist_ok=True)

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{test_db}",
        "UPLOAD_FOLDER": upload_dir,
        "SECRET_KEY": "test-secret-key-123"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    # Clean up test files
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except Exception:
            pass
    if os.path.exists(upload_dir):
        import shutil
        shutil.rmtree(upload_dir, ignore_errors=True)

@pytest.fixture(scope="module")
def client(app_instance):
    return app_instance.test_client()

# Helper to create a PDF with text
def create_test_pdf(text: str) -> io.BytesIO:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), text, fontsize=11)
    buffer = io.BytesIO(doc.tobytes())
    doc.close()
    buffer.seek(0)
    return buffer

# Helper to create a PNG image with text
def create_test_image(text: str) -> io.BytesIO:
    img = Image.new("RGB", (800, 400), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((30, 40), text, fill="black")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Auth token fixture
auth_token = None
user_id = None
created_report_ids = []

def test_01_user_registration(client):
    global auth_token, user_id
    res = client.post("/api/auth/register", json={
        "name": "Dr. Alex Rivera",
        "email": "alex.rivera@mediscan.ai",
        "password": "Password123"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert "token" in data
    assert data["user"]["email"] == "alex.rivera@mediscan.ai"
    auth_token = data["token"]
    user_id = data["user"]["id"]

def test_02_user_login(client):
    res = client.post("/api/auth/login", json={
        "email": "alex.rivera@mediscan.ai",
        "password": "Password123"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "token" in data

def test_03_invalid_login(client):
    res = client.post("/api/auth/login", json={
        "email": "alex.rivera@mediscan.ai",
        "password": "WrongPassword999"
    })
    assert res.status_code == 401
    data = res.get_json()
    assert data["success"] is False

def test_04_pdf_upload(client):
    pdf_text = (
        "COMPLETE BLOOD COUNT (CBC) REPORT. Patient Name: Test Case 1. "
        "Hemoglobin: 14.2 g/dL. Total WBC: 7,200 /mcL. Platelet Count: 280,000 /mcL. "
        "Neutrophils: 64%, Lymphocytes: 28%. Red blood cell indices normocytic normochromic."
    )
    pdf_stream = create_test_pdf(pdf_text)
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post(
        "/api/reports/upload",
        data={"file": (pdf_stream, "test_cbc_report.pdf")},
        content_type="multipart/form-data",
        headers=headers
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert data["report"]["predicted_category"] == "Blood Test"
    created_report_ids.append(data["report"]["id"])

def test_05_image_upload(client):
    img_text = (
        "CARDIOLOGY CONSULTATION & ECG EXAMINATION.\n"
        "Patient: Heart patient 44.\n"
        "Sinus rhythm rate 76 bpm. LVEF 60%.\n"
        "Normal left ventricular systolic function.\n"
        "No acute ST elevation or depression."
    )
    img_stream = create_test_image(img_text)
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post(
        "/api/reports/upload",
        data={"file": (img_stream, "cardio_scan.png")},
        content_type="multipart/form-data",
        headers=headers
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    created_report_ids.append(data["report"]["id"])

def test_06_ocr_text_extraction(client):
    # Verify that image upload extracted meaningful text
    headers = {"Authorization": f"Bearer {auth_token}"}
    report_id = created_report_ids[-1]
    res = client.get(f"/api/reports/{report_id}", headers=headers)
    assert res.status_code == 200
    data = res.get_json()
    extracted = data["report"]["extracted_text"]
    assert len(extracted) > 20

def test_07_blood_test_classification(client):
    text = (
        "Apex Diagnostics - Hematology Lab Report. "
        "Complete Blood Count (CBC). Hemoglobin 10.5 g/dL (Low). "
        "Packed Cell Volume (PCV): 32%. Total Leukocytes: 9,200 /uL. "
        "Platelet count: 210,000 /uL. MCV 74 fL. ESR 30 mm/hr. Hypochromia noted."
    )
    stream = create_test_pdf(text)
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post(
        "/api/reports/upload",
        data={"file": (stream, "blood_work.pdf")},
        content_type="multipart/form-data",
        headers=headers
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["report"]["predicted_category"] == "Blood Test"
    assert data["report"]["confidence_score"] > 0.5
    created_report_ids.append(data["report"]["id"])

def test_08_diabetes_classification(client):
    text = (
        "Metro Health - Diabetes Profile. "
        "Fasting Blood Sugar (FBS): 195 mg/dL. Postprandial Blood Sugar (PPBS): 278 mg/dL. "
        "Glycated Hemoglobin (HbA1c): 9.2%. Estimated Average Glucose: 217 mg/dL. "
        "Urine glucose present (2+). Poorly controlled Type 2 Diabetes Mellitus."
    )
    stream = create_test_pdf(text)
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post(
        "/api/reports/upload",
        data={"file": (stream, "diabetes_report.pdf")},
        content_type="multipart/form-data",
        headers=headers
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["report"]["predicted_category"] == "Diabetes"
    created_report_ids.append(data["report"]["id"])

def test_09_cardiology_classification(client):
    text = (
        "Department of Cardiology - Echocardiography Report. "
        "12-Lead Electrocardiogram shows sinus rhythm at 72 bpm. "
        "Transthoracic 2D Echo demonstrates Left Ventricular Ejection Fraction (LVEF) 45%. "
        "Mild mitral regurgitation. Serum Troponin I: 120 ng/L. CK-MB elevated."
    )
    stream = create_test_pdf(text)
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post(
        "/api/reports/upload",
        data={"file": (stream, "cardio_echo.pdf")},
        content_type="multipart/form-data",
        headers=headers
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["report"]["predicted_category"] == "Cardiology"
    created_report_ids.append(data["report"]["id"])

def test_10_radiology_classification(client):
    text = (
        "DEPARTMENT OF RADIOLOGY & IMAGING. "
        "Procedure: Chest X-ray (CXR) PA View. "
        "Findings: Trachea is midline. Cardiothoracic ratio is normal. "
        "There is a patchy consolidation in right lower lobe with blunting of costophrenic angle. "
        "Impression: Radiological evidence of right lower lobe pneumonia."
    )
    stream = create_test_pdf(text)
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post(
        "/api/reports/upload",
        data={"file": (stream, "chest_xray.pdf")},
        content_type="multipart/form-data",
        headers=headers
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["report"]["predicted_category"] == "Radiology"
    created_report_ids.append(data["report"]["id"])

def test_11_kidney_classification(client):
    text = (
        "Nephrology Clinic - Renal Function Test (RFT/KFT). "
        "Serum Creatinine: 3.10 mg/dL (High). Blood Urea Nitrogen (BUN): 52 mg/dL. "
        "Estimated Glomerular Filtration Rate (eGFR): 22 mL/min/1.73m2. "
        "Urinalysis reveals proteinuria 2+ and microscopic hematuria. Stage 4 Chronic Kidney Disease."
    )
    stream = create_test_pdf(text)
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post(
        "/api/reports/upload",
        data={"file": (stream, "renal_profile.pdf")},
        content_type="multipart/form-data",
        headers=headers
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["report"]["predicted_category"] == "Kidney"
    created_report_ids.append(data["report"]["id"])

def test_12_liver_classification(client):
    text = (
        "Gastroenterology Lab - Liver Function Test (LFT). "
        "Total Bilirubin: 3.8 mg/dL. Direct Bilirubin: 2.4 mg/dL. "
        "SGPT / ALT: 215 U/L. SGOT / AST: 180 U/L. Alkaline Phosphatase (ALP): 195 U/L. "
        "Serum Albumin: 3.1 g/dL. Acute hepatocellular injury with cholestatic jaundice."
    )
    stream = create_test_pdf(text)
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post(
        "/api/reports/upload",
        data={"file": (stream, "liver_panel.pdf")},
        content_type="multipart/form-data",
        headers=headers
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["report"]["predicted_category"] == "Liver"
    created_report_ids.append(data["report"]["id"])

def test_13_empty_document_handling(client):
    # Blank PDF with no text
    doc = fitz.open()
    doc.new_page()
    empty_stream = io.BytesIO(doc.tobytes())
    doc.close()
    empty_stream.seek(0)

    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post(
        "/api/reports/upload",
        data={"file": (empty_stream, "blank_document.pdf")},
        content_type="multipart/form-data",
        headers=headers
    )
    assert res.status_code == 422
    data = res.get_json()
    assert data["success"] is False
    assert "insufficient" in data["message"].lower()

def test_14_invalid_file_handling(client):
    bad_stream = io.BytesIO(b"This is an invalid text file format.")
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.post(
        "/api/reports/upload",
        data={"file": (bad_stream, "notes.txt")},
        content_type="multipart/form-data",
        headers=headers
    )
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False
    assert "unsupported" in data["message"].lower()

def test_15_report_history(client):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = client.get("/api/reports?category=all", headers=headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["count"] >= 6

    # Test filtering by category
    filter_res = client.get("/api/reports?category=Kidney", headers=headers)
    assert filter_res.status_code == 200
    filter_data = filter_res.get_json()
    for rep in filter_data["reports"]:
        assert rep["predicted_category"] == "Kidney"

def test_16_report_deletion(client):
    headers = {"Authorization": f"Bearer {auth_token}"}
    target_id = created_report_ids.pop()
    res = client.delete(f"/api/reports/{target_id}", headers=headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True

    # Verify report is gone
    check_res = client.get(f"/api/reports/{target_id}", headers=headers)
    assert check_res.status_code == 404

def test_17_pdf_result_download(client):
    headers = {"Authorization": f"Bearer {auth_token}"}
    target_id = created_report_ids[0]
    res = client.get(f"/api/reports/{target_id}/download", headers=headers)
    assert res.status_code == 200
    assert res.content_type == "application/pdf"
    assert len(res.data) > 500  # Non-trivial PDF size

def test_18_unauthorized_access_prevention(app_instance):
    # Attempt to access reports with fresh client without auth token or session
    unauth_client = app_instance.test_client()
    res = unauth_client.get("/api/reports")
    assert res.status_code == 401
    data = res.get_json()
    assert data["success"] is False
    assert "authentication required" in data["message"].lower()
