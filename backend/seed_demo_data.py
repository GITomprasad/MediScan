"""
MediScan AI - Demo Data Seeder
Populates initial verified user account and categorized medical records
for instant presentation and testing.
"""

import os
from app import create_app
from app.models import db, User, Report
from app.ml.classifier import classifier_service

app = create_app()

sample_reports_data = [
    {
        "filename": "CBC_Hematology_Profile_JaneDoe.pdf",
        "category": "Blood Test",
        "text": (
            "METRO HEALTH LABORATORIES - COMPLETE BLOOD COUNT (CBC). "
            "Patient: Jane Doe, Age: 34, Gender: Female. "
            "Hemoglobin (Hb): 13.5 g/dL (Ref: 12.0 - 15.5). "
            "Total WBC Count: 7,100 cells/mcL (Ref: 4,000 - 11,000). "
            "Platelet Count: 260,000 /mcL (Ref: 150,000 - 450,000). "
            "Hematocrit (PCV): 40.2%. MCV: 86.4 fL, MCH: 29.1 pg, MCHC: 33.4 g/dL. "
            "Differential: Neutrophils 62%, Lymphocytes 29%, Monocytes 5%, Eosinophils 3%, Basophils 1%. "
            "Erythrocyte Sedimentation Rate (ESR): 14 mm/hr. "
            "Impression: Normal Complete Blood Count within expected physiological reference intervals."
        )
    },
    {
        "filename": "Diabetes_HbA1c_Monitoring_Report.pdf",
        "category": "Diabetes",
        "text": (
            "ENDOCRINOLOGY CLINICAL REPORT: DIABETIC METABOLIC PANEL. "
            "Patient: Robert Jenkins, Age: 52. "
            "Fasting Plasma Glucose (FBS): 168 mg/dL (Ref: 70 - 99 mg/dL, High). "
            "Postprandial Blood Sugar (PPBS 2-hour): 242 mg/dL (Ref: < 140 mg/dL, High). "
            "Glycated Hemoglobin (HbA1c): 8.6% (Ref: < 5.7%, High). "
            "Estimated Average Glucose (eAG): 200 mg/dL. "
            "Urine Glucose: Positive (2+). Urine Ketones: Negative. "
            "Impression: Sub-optimally controlled Type 2 Diabetes Mellitus with significant hyperglycemia."
        )
    },
    {
        "filename": "Echocardiogram_and_ECG_Analysis.pdf",
        "category": "Cardiology",
        "text": (
            "DEPARTMENT OF CARDIOLOGY - 12-LEAD ECG & 2D ECHOCARDIOGRAM. "
            "Patient: Marcus Rivera, Age: 61. "
            "Electrocardiogram: Sinus rhythm at 74 beats per minute. Normal PR interval (158 ms). "
            "Transthoracic 2D Echocardiogram: "
            "Left Ventricular Ejection Fraction (LVEF): 58% (Normal systolic performance). "
            "Left ventricular internal dimensions within normal limits. "
            "Aortic and mitral valve leaflets show normal excursion without significant regurgitation or stenosis. "
            "Serum High-Sensitivity Cardiac Troponin I: 8.2 ng/L (Normal < 14.0 ng/L). "
            "Impression: Normal cardiac systolic function and resting electrocardiogram."
        )
    },
    {
        "filename": "Chest_Radiograph_PA_View.png",
        "category": "Radiology",
        "text": (
            "APEX IMAGING - DEPARTMENT OF RADIOLOGY. "
            "PROCEDURE: CHEST RADIOGRAPH (X-RAY PA VIEW). "
            "Clinical History: Persistent cough, mild low-grade pyrexia. "
            "Findings: The cardiac shadow is normal in size and contour with cardiothoracic ratio < 0.5. "
            "Mediastinum and hila are unremarkable. Trachea is central. "
            "Subtle patchy alveolar consolidation noted in the right lower lung zone. "
            "Both costophrenic angles and cardiophrenic sulci are sharp. "
            "Impression: Right lower zone pneumonic patch without evidence of pleural effusion or pneumothorax."
        )
    },
    {
        "filename": "Renal_Function_Test_KFT_Panel.pdf",
        "category": "Kidney",
        "text": (
            "NEPHROLOGY SERVICES - RENAL FUNCTION TEST (RFT / KFT). "
            "Patient: David Miller, Age: 58. "
            "Serum Creatinine: 2.45 mg/dL (Ref: 0.70 - 1.30 mg/dL, High). "
            "Blood Urea Nitrogen (BUN): 44 mg/dL (Ref: 7 - 20 mg/dL, High). "
            "Estimated Glomerular Filtration Rate (eGFR): 29 mL/min/1.73m2 (Stage 4 Chronic Kidney Disease). "
            "Serum Uric Acid: 8.1 mg/dL. Serum Sodium: 138 mEq/L, Potassium: 4.9 mEq/L. "
            "Urinalysis: Proteinuria 2+ detected on dipstick. "
            "Impression: Moderate to severe renal impairment with elevated azotemia parameters."
        )
    },
    {
        "filename": "Liver_Function_Test_Enzyme_Panel.pdf",
        "category": "Liver",
        "text": (
            "CAREWELL PATHOLOGY - HEPATOBILIARY PANEL (LFT). "
            "Patient: Sarah Connor, Age: 47. "
            "Serum Total Bilirubin: 3.1 mg/dL (Ref: 0.2 - 1.2 mg/dL, Elevated). "
            "Direct Bilirubin: 1.9 mg/dL. "
            "Alanine Aminotransferase (ALT / SGPT): 192 U/L (Ref: < 45 U/L, High). "
            "Aspartate Aminotransferase (AST / SGOT): 165 U/L (Ref: < 40 U/L, High). "
            "Alkaline Phosphatase (ALP): 180 U/L. Total Protein: 7.1 g/dL, Albumin: 3.4 g/dL. "
            "Impression: Acute hepatocellular injury pattern with cholestatic elevation."
        )
    }
]

def seed():
    with app.app_context():
        # Create tables
        db.create_all()

        # Check or create demo user
        demo_user = User.query.filter_by(email="alex.rivera@mediscan.ai").first()
        if not demo_user:
            demo_user = User(
                name="Dr. Alex Rivera",
                email="alex.rivera@mediscan.ai"
            )
            demo_user.set_password("Password123")
            db.session.add(demo_user)
            db.session.commit()
            print(f"[Seed] Created demo user: {demo_user.email} (Password: Password123)")
        else:
            print(f"[Seed] Demo user already exists: {demo_user.email}")

        # Check if reports exist
        existing_count = Report.query.filter_by(user_id=demo_user.id).count()
        if existing_count == 0:
            upload_dir = app.config['UPLOAD_FOLDER']
            os.makedirs(upload_dir, exist_ok=True)

            for item in sample_reports_data:
                dummy_path = os.path.join(upload_dir, f"demo_{item['filename']}")
                with open(dummy_path, "w", encoding="utf-8") as f:
                    f.write(item["text"])

                # Run ML model on the text to get real prediction & confidence
                ml_result = classifier_service.classify(item["text"])

                rep = Report(
                    user_id=demo_user.id,
                    filename=item["filename"],
                    file_path=dummy_path,
                    file_size=len(item["text"].encode('utf-8')),
                    mime_type="application/pdf" if item["filename"].endswith(".pdf") else "image/png",
                    extracted_text=item["text"],
                    predicted_category=ml_result["predicted_category"],
                    confidence_score=ml_result["confidence_score"],
                    processing_status="completed"
                )
                db.session.add(rep)

            db.session.commit()
            print(f"[Seed] Successfully added {len(sample_reports_data)} demo classified reports.")
        else:
            print(f"[Seed] Demo user already has {existing_count} reports.")

if __name__ == "__main__":
    seed()
