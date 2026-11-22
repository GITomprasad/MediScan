# MediScan AI – Intelligent Medical Report Classification System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-v4-38B2AC.svg)](https://tailwindcss.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9-F7931E.svg)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/Tests-18%20Passed-brightgreen.svg)]()

MediScan AI is an end-to-end, full-stack medical document classification platform. Users can upload medical test reports in PDF, JPG, JPEG, and PNG formats. The system extracts clinical text using PyMuPDF and OCR, cleans and vectorizes the content with TF-IDF, and classifies the document using a calibrated machine learning model across six clinical categories with high confidence scoring.

> [!IMPORTANT]
> **Clinical Disclaimer:** MediScan AI is an automated document indexing and categorization tool designed for medical record organization and administrative workflow routing. It **DOES NOT** provide medical diagnosis, clinical prognosis, disease staging, or treatment recommendations. Always consult a licensed healthcare practitioner for medical guidance.

---

## 1. Supported Medical Categories

The application classifies documents into these six categories:

1. **Blood Test** – Complete Blood Count (CBC), hemoglobin, hematocrit, platelet count, WBC differential, ESR, coagulation PT/INR.
2. **Diabetes** – Fasting blood glucose (FBS), postprandial glucose (PPBS), glycated hemoglobin (HbA1c), oral glucose tolerance tests (OGTT), insulin.
3. **Cardiology** – 12-lead electrocardiograms (ECG/EKG), 2D echocardiograms (LVEF), cardiac enzymes, Troponin I/T, CK-MB.
4. **Radiology** – Chest radiographs (CXR), CT scans (brain, thorax, abdomen), MRI studies, ultrasound (USG), and mammography.
5. **Kidney** – Renal function tests (RFT/KFT), serum creatinine, blood urea nitrogen (BUN), eGFR, urinalysis, 24-hr proteinuria.
6. **Liver** – Liver function tests (LFT), total/direct bilirubin, transaminases (SGPT/ALT, SGOT/AST), ALP, GGT, albumin, and viral hepatitis markers.

---

## 2. Technology Stack

- **Frontend:**
  - React 19 + Vite
  - Tailwind CSS v4 (Healthcare SaaS modern aesthetic)
  - Lucide React icons
  - Recharts (Interactive category distribution & monthly activity charts)
  - React Router v7
  - Axios with JWT/Session cookie authentication interceptors
- **Backend:**
  - Python Flask + REST API
  - Flask-CORS + Werkzeug Security
  - SQLite + SQLAlchemy ORM
  - Session-based and Bearer JWT token authentication
- **Machine Learning & NLP:**
  - Scikit-Learn
  - TF-IDF Vectorizer (Unigram + Bigram, sublinear term frequency)
  - Multinomial Logistic Regression with Calibrated probabilities
  - Real test-set evaluation (Accuracy: 93.3%, Precision: 94.3%, Recall: 93.3%, F1-Score: 93.4%)
- **Document Processing & OCR:**
  - PyMuPDF (`pymupdf` / `fitz`) for digital PDF text extraction
  - RapidOCR (ONNX runtime) + Tesseract OCR fallback for scanned PDFs and image files
  - Pillow (`PIL`) for image preprocessing (grayscale, contrast enhancement, sharpening)
  - ReportLab for generating official PDF summary certificates

---

## 3. Project Structure

```
mediscan-ai/
├── frontend/
│   ├── src/
│   │   ├── components/       # ProtectedRoute, UI cards
│   │   ├── context/          # AuthContext (login, register, session)
│   │   ├── layouts/          # DashboardLayout, PublicNavbar, PublicFooter
│   │   ├── pages/            # LandingPage, Login, Register, Dashboard, Upload, Results, History, Profile, Metrics
│   │   ├── services/         # Axios API client with interceptors
│   │   └── App.jsx           # Main application routing
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── ml/               # MedicalDocumentClassifier inference service
│   │   ├── models/           # User and Report SQLAlchemy models
│   │   ├── routes/           # Auth, Reports, and Dashboard REST endpoints
│   │   ├── services/         # DocumentService (OCR/PyMuPDF), PDFGenerator (ReportLab)
│   │   ├── utils/            # Authentication & token verification helpers
│   │   └── __init__.py       # Flask app factory, CORS, and DB init
│   ├── dataset/              # Labeled medical report dataset (240 samples)
│   ├── trained_models/       # Saved classifier, vectorizer, and metrics JSON
│   ├── tests/                # 18 comprehensive pytest test cases
│   ├── generate_dataset.py   # Dataset generation script
│   ├── train_model.py        # ML training and evaluation script
│   ├── seed_demo_data.py     # Demo user and initial classified reports seeder
│   ├── requirements.txt      # Python dependencies
│   └── run.py                # Flask server entry point
│
├── sample_reports/           # Ready-to-use sample PDFs and images for testing
├── .env.example
├── .gitignore
└── README.md
```

---

## 4. Quick Start & Installation (Windows / macOS / Linux)

### Step 1: Clone or navigate to the repository
```bash
cd "medical report classification"
```

### Step 2: Set up Backend
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# (Optional) Retrain model and seed demo database
python train_model.py
python seed_demo_data.py

# Start Flask Backend server
python run.py
```
Backend API will be running at: `http://127.0.0.1:5000`

### Step 3: Set up Frontend
Open a new terminal window:
```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
Frontend will be running at: `http://localhost:5173`

---

## 5. Verified Demo Credentials

For quick presentation and evaluation, use the pre-seeded demo account:

- **Email:** `alex.rivera@mediscan.ai`
- **Password:** `Password123`
*(A "Fill Verified Demo Credentials" button is also provided directly on the Login page)*

---

## 6. Testing Instructions

To run the complete automated test suite covering all 18 required scenarios:

```bash
cd backend
python -m pytest -v tests/test_backend.py
```

### Verified Test Cases:
1. `test_01_user_registration` - User signup and password hashing
2. `test_02_user_login` - User authentication and token issuance
3. `test_03_invalid_login` - Rejection of invalid credentials
4. `test_04_pdf_upload` - Native PDF extraction and ingestion
5. `test_05_image_upload` - PNG/JPG image upload and processing
6. `test_06_ocr_text_extraction` - OCR text recognition on images
7. `test_07_blood_test_classification` - CBC / Hematology classification
8. `test_08_diabetes_classification` - Glucose & HbA1c classification
9. `test_09_cardiology_classification` - ECG & Troponin classification
10. `test_10_radiology_classification` - X-Ray & imaging report classification
11. `test_11_kidney_classification` - Creatinine & BUN classification
12. `test_12_liver_classification` - Bilirubin & LFT classification
13. `test_13_empty_document_handling` - Clean rejection of blank documents
14. `test_14_invalid_file_handling` - Rejection of unsupported file types
15. `test_15_report_history` - Querying and filtering report history
16. `test_16_report_deletion` - Secure cascade deletion of reports
17. `test_17_pdf_result_download` - ReportLab PDF summary generation
18. `test_18_unauthorized_access_prevention` - Protection of private endpoints

---

## 7. Sample Test Reports

You can test document uploading with the files in `sample_reports/`:
- `sample_reports/blood_test_cbc_sample.pdf`
- `sample_reports/diabetes_glucose_sample.pdf`
- `sample_reports/cardiology_ecg_sample.pdf`
- `sample_reports/radiology_xray_scan.png`
- `sample_reports/kidney_rft_panel.pdf`
- `sample_reports/liver_enzymes_lft.pdf`
- `sample_reports/blank_unsupported_test.pdf` (Tests rejection of blank files)

---

## 8. REST API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/api/auth/register` | Register a new user | No |
| POST | `/api/auth/login` | Login and obtain session / token | No |
| POST | `/api/auth/logout` | Clear user session | Yes |
| GET | `/api/auth/me` | Fetch authenticated user profile | Yes |
| PUT | `/api/auth/password` | Update account password | Yes |
| GET | `/api/dashboard/stats` | Aggregated report counts and metrics | Yes |
| GET | `/api/dashboard/recent` | Recent 5 classifications | Yes |
| POST | `/api/reports/upload` | Upload PDF/image, run OCR & classify | Yes |
| GET | `/api/reports` | List reports with search, filter, and sort | Yes |
| GET | `/api/reports/:id` | Fetch detailed report and extracted text | Yes |
| DELETE | `/api/reports/:id` | Delete report and local file | Yes |
| GET | `/api/reports/:id/download` | Download generated PDF summary certificate | Yes |
| GET | `/api/analytics/categories` | Category distribution for Recharts | Yes |
| GET | `/api/analytics/monthly` | Monthly upload trend data | Yes |
| GET | `/api/analytics/model-metrics` | Actual test-set ML evaluation metrics | No |
| GET | `/api/health` | API health check | No |

---

## 9. Security & Compliance Measures

- **Password Hashing:** PBKDF2 with SHA-256 via Werkzeug.
- **Sanitized Uploads:** File paths generated using `secure_filename` and unique UUIDs to prevent directory traversal attacks.
- **Tenant Isolation:** Users can only query, inspect, download, or delete their own documents.
- **Payload Boundaries:** Maximum upload file size capped at 10 MB.
- **PHI Log Privacy:** Extracted clinical content is never printed to application runtime logs.
