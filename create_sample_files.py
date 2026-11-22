"""
Generate sample PDF and image documents for testing upload and classification.
"""

import os
import io
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

samples = {
    "blood_test_cbc_sample.pdf": (
        "METRO HEALTHCARE DIAGNOSTICS - HEMATOLOGY REPORT\n\n"
        "PATIENT: Robert Miller, Age: 42, Sex: Male\n"
        "REFERRED BY: Dr. S. Patel, MD\n\n"
        "TEST: COMPLETE BLOOD COUNT (CBC) WITH DIFFERENTIAL\n"
        "----------------------------------------------------------\n"
        "Hemoglobin (Hb): 14.8 g/dL        (Normal: 13.0 - 17.0)\n"
        "RBC Count: 4.85 mil/mcL           (Normal: 4.5 - 5.9)\n"
        "Hematocrit (PCV): 44.2%           (Normal: 40.0 - 52.0)\n"
        "Mean Corpuscular Volume (MCV): 91.1 fL (Normal: 80 - 100)\n"
        "MCH: 30.5 pg                      (Normal: 27 - 33)\n"
        "MCHC: 33.5 g/dL                   (Normal: 32 - 36)\n"
        "Total Leukocyte Count (WBC): 6,900 /mcL (Normal: 4,500 - 11,000)\n"
        "Platelet Count: 275,000 /mcL      (Normal: 150,000 - 450,000)\n\n"
        "DIFFERENTIAL COUNT:\n"
        "Neutrophils: 61% | Lymphocytes: 29% | Monocytes: 6% | Eosinophils: 3% | Basophils: 1%\n"
        "Erythrocyte Sedimentation Rate (ESR): 12 mm/1st hr\n\n"
        "PERIPHERAL BLOOD FILM: Normocytic normochromic RBCs. Adequate platelets."
    ),
    "diabetes_glucose_sample.pdf": (
        "APEX ENDOCRINE CLINIC - DIABETIC METABOLIC INVESTIGATION\n\n"
        "PATIENT: Sarah Jenkins, Age: 55, Female\n"
        "PHYSICIAN: Dr. Michael Chang, MD (Endocrinology)\n\n"
        "TESTS PERFORMED:\n"
        "----------------------------------------------------------\n"
        "1. Fasting Plasma Glucose (FBS): 176 mg/dL     [Ref: 70 - 100, HIGH]\n"
        "2. Post-Prandial Blood Sugar (PPBS): 254 mg/dL [Ref: < 140, HIGH]\n"
        "3. Glycated Hemoglobin (HbA1c): 8.9%          [Ref: < 5.7%, POOR CONTROL]\n"
        "4. Estimated Average Glucose (eAG): 208 mg/dL\n"
        "5. Urine Glucose: 2+ (Positive)\n"
        "6. Urine Ketones: Negative\n"
        "7. Fasting Serum Insulin: 19.2 uIU/mL (Elevated)\n\n"
        "IMPRESSION: Consistent with poorly regulated Type 2 Diabetes Mellitus with chronic hyperglycemia."
    ),
    "cardiology_ecg_sample.pdf": (
        "ST. JUDE HEART INSTITUTE - CARDIOLOGY REPORT\n\n"
        "PATIENT: Thomas Wayne, Age: 63, Male\n"
        "INVESTIGATION: 12-LEAD ELECTROCARDIOGRAM & 2D ECHOCARDIOGRAM\n"
        "----------------------------------------------------------\n"
        "Resting ECG Parameters:\n"
        "Heart Rate: 72 bpm, Rhythm: Regular Sinus Rhythm\n"
        "PR Interval: 162 ms, QRS Duration: 86 ms, QTc: 418 ms\n"
        "ST-T Wave Assessment: No acute ST elevation, depression, or pathological Q waves.\n\n"
        "Transthoracic 2D Echocardiogram:\n"
        "Left Ventricular Ejection Fraction (LVEF): 56% (Preserved systolic function)\n"
        "LVIDd: 4.7 cm, LVIDs: 3.0 cm, Interventricular Septum: 1.05 cm\n"
        "Valvular Function: Normal aortic and mitral valve leaflet motion. Trivial mitral regurgitation.\n"
        "Cardiac Biomarkers: High-Sensitivity Troponin I: 6.4 pg/mL (Reference: < 14.0 pg/mL)\n\n"
        "IMPRESSION: Preserved left ventricular systolic performance without acute ischemic changes."
    ),
    "kidney_rft_panel.pdf": (
        "CITY CENTRAL LAB - RENAL FUNCTION TEST (RFT / KFT)\n\n"
        "PATIENT: Arthur Dent, Age: 60, Male\n"
        "DEPARTMENT: NEPHROLOGY\n"
        "----------------------------------------------------------\n"
        "Serum Creatinine: 2.95 mg/dL                  [Ref: 0.70 - 1.30, HIGH]\n"
        "Blood Urea Nitrogen (BUN): 49 mg/dL           [Ref: 7 - 20, HIGH]\n"
        "Serum Urea: 105 mg/dL\n"
        "Estimated Glomerular Filtration Rate (eGFR): 23 mL/min/1.73m2 [CKD Stage 4]\n"
        "Serum Uric Acid: 8.8 mg/dL                    [Ref: 3.5 - 7.2, HIGH]\n"
        "Electrolytes: Sodium 137 mEq/L, Potassium 5.1 mEq/L, Chloride 101 mEq/L\n\n"
        "URINALYSIS ROUTINE & MICROSCOPY:\n"
        "Protein / Albumin: 2+ Positive | RBCs: 4-6 /HPF | Granular Casts: 2-3 /LPF\n\n"
        "IMPRESSION: Renal failure parameters indicating Stage 4 Chronic Kidney Disease."
    ),
    "liver_enzymes_lft.pdf": (
        "BIOQUEST LABORATORIES - LIVER FUNCTION TEST (LFT)\n\n"
        "PATIENT: Emily Clark, Age: 39, Female\n"
        "CONSULTANT: Dr. Rachel Green, MD\n"
        "----------------------------------------------------------\n"
        "Total Serum Bilirubin: 3.4 mg/dL              [Ref: 0.2 - 1.2, HIGH]\n"
        "Direct (Conjugated) Bilirubin: 2.2 mg/dL       [Ref: 0.0 - 0.3, HIGH]\n"
        "Indirect Bilirubin: 1.2 mg/dL\n"
        "SGPT / ALT (Alanine Aminotransferase): 235 U/L [Ref: 7 - 45, HIGH]\n"
        "SGOT / AST (Aspartate Aminotransferase): 188 U/L [Ref: 10 - 40, HIGH]\n"
        "Alkaline Phosphatase (ALP): 195 U/L           [Ref: 44 - 147, HIGH]\n"
        "Gamma-Glutamyl Transferase (GGT): 150 U/L\n"
        "Total Protein: 6.9 g/dL | Serum Albumin: 3.2 g/dL | A/G Ratio: 0.86\n\n"
        "IMPRESSION: Pattern indicative of acute hepatocellular liver injury with cholestatic jaundice."
    ),
    "blank_unsupported_test.pdf": (
        "   "  # Empty text for testing error handling
    )
}

# Create PDFs
for fname, content in samples.items():
    fpath = os.path.join(OUTPUT_DIR, fname)
    doc = fitz.open()
    page = doc.new_page()
    if content.strip():
        page.insert_text((45, 60), content, fontsize=10)
    doc.save(fpath)
    doc.close()
    print(f"Created: {fpath}")

# Create Image for Radiology scan
img_path = os.path.join(OUTPUT_DIR, "radiology_xray_scan.png")
img = Image.new("RGB", (900, 600), color=(250, 252, 255))
draw = ImageDraw.Draw(img)

xray_text = (
    "DEPARTMENT OF RADIOLOGY & MEDICAL IMAGING\n\n"
    "PROCEDURE: CHEST RADIOGRAPH (X-RAY PA VIEW)\n"
    "PATIENT: William Murdoch, Age: 50, Male\n"
    "CLINICAL INDICATION: Productive cough, chest discomfort\n\n"
    "RADIOLOGICAL FINDINGS:\n"
    "- Cardiothoracic ratio is normal (< 0.50).\n"
    "- Trachea is midline. Mediastinum unremarkable.\n"
    "- Patchy alveolar consolidation identified in the right lower lung field.\n"
    "- Left lung parenchyma is clear with normal bronchovascular markings.\n"
    "- Right costophrenic angle blunted, indicating mild reactive pleural effusion.\n"
    "- Visualized osseous thorax and diaphragmatic contours are preserved.\n\n"
    "IMPRESSION: Right lower lobe pneumonia with associated parapneumonic effusion."
)

draw.text((40, 50), xray_text, fill=(20, 30, 45))
img.save(img_path)
print(f"Created: {img_path}")
