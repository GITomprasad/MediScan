"""
MediScan AI - Medical Reports Dataset Generator
Generates realistic, diverse clinical reports across 6 medical categories:
1. Blood Test
2. Diabetes
3. Cardiology
4. Radiology
5. Kidney
6. Liver
"""

import csv
import os
import random

DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset", "medical_reports_dataset.csv")

categories = {
    "Blood Test": [
        "COMPLETE BLOOD COUNT (CBC) REPORT. Patient Name: Jane Doe. Hemoglobin: 13.8 g/dL (Ref: 12.0 - 15.5). RBC Count: 4.5 million/mcL. Hematocrit (PCV): 41.2%. MCV: 88.5 fL, MCH: 29.4 pg, MCHC: 33.2 g/dL. Total Leukocyte Count (WBC): 6,800 cells/mcL. Differential count: Neutrophils 62%, Lymphocytes 28%, Monocytes 6%, Eosinophils 3%, Basophils 1%. Platelet Count: 245,000 /mcL. Peripheral blood smear shows normocytic normochromic red cells with normal morphology.",
        "HEMATOLOGY EXAMINATION: CBC with ESR. Hemoglobin: 9.4 g/dL (Low, microcytic hypochromic pattern). Hematocrit: 29.1%. MCV: 72.1 fL (Low), MCH: 22.0 pg (Low). Total WBC: 8,400 /uL. Platelets: 380,000 /uL. Erythrocyte Sedimentation Rate (ESR): 34 mm/hr (Elevated). Serum Ferritin: 11 ng/mL (Low). Serum Iron: 38 mcg/dL (Low). Total Iron Binding Capacity (TIBC): 440 mcg/dL. Impression: Consistent with Iron Deficiency Anemia.",
        "ROUTINE BLOOD WORK & COAGULATION PROFILE. Prothrombin Time (PT): 12.4 seconds (Control: 11.8). INR (International Normalized Ratio): 1.08. Activated Partial Thromboplastin Time (APTT): 31.0 seconds. Fibrinogen: 280 mg/dL. Bleeding Time: 2 mins 30 secs, Clotting Time: 6 mins. Platelet count adequate at 210,000 /uL. Hemoglobin: 14.2 g/dL.",
        "BLOOD MORPHOLOGY & RETICULOCYTE COUNT. Reticulocyte Count: 2.4% (Elevated). Absolute Reticulocyte Count: 98,000 /uL. Vitamin B12: 145 pg/mL (Deficient). Folate: 7.2 ng/mL. Peripheral blood film reveals macrocytosis, hypersegmented neutrophils, and mild anisopoikilocytosis. Megaloblastic blood picture noted.",
        "HEMATOLOGY LAB REPORT. Complete Hemogram: Hb 11.2 g/dL, Total RBC 3.8 x 10^12/L, PCV 34%. WBC 11,500 /cumm with mild neutrophilic leukocytosis (Neutrophils 78%, Lymphocytes 16%). Absolute Neutrophil Count (ANC): 8,970. Platelets: 185,000. ESR: 28 mm in 1st hour.",
        "BONE MARROW & BLOOD PROFILE. Patient presenting with fatigue and pallor. CBC reveals Hemoglobin 8.1 g/dL, Hematocrit 25%, RBC 2.9 million, MCV 86 fL. Platelet count: 95,000 /uL (mild thrombocytopenia). Leukocytes: 3,200 /uL (leukopenia). Red cell distribution width (RDW): 16.8%. Serum transferrin saturation: 22%.",
        "COAGULATION STUDY & D-DIMER. D-Dimer Quantitative: 240 ng/mL (Normal < 500 ng/mL FEU). Fibrinogen degradation products (FDP): negative. PT: 13.0 sec, INR: 1.04, PTT: 33.2 sec. Routine CBC confirms normal platelet count of 260,000 /mcL and Hemoglobin of 15.1 g/dL.",
        "HEMOGLOBIN ELECTROPHORESIS & BLOOD PANEL. Hb A1: 96.8%, Hb A2: 2.2%, Hb F: 0.9%, Abnormal hemoglobin variants: Not detected. Complete blood count shows Hemoglobin 12.8 g/dL, Hematocrit 39%, MCV 84 fL, MCH 28 pg. Normal red blood cell indices.",
        "BLOOD GAS ANALYSIS & HEMOGRAM. Arterial Blood Gas: pH 7.41, pCO2 39 mmHg, pO2 94 mmHg, HCO3 24.2 mmol/L, Base excess +0.5. Co-oximetry: Oxyhemoglobin 97.4%, Methemoglobin 0.6%. Venous CBC: Total WBC 7,100 /uL, Hb 14.5 g/dL, Platelets 220,000 /uL.",
        "SPECIALIZED HEMATOLOGY INVESTIGATION. Cold Agglutinin Titre: Negative. Coombs Test (Direct Antiglobulin Test): Negative. Coombs Test Indirect: Negative. Hemoglobin: 12.1 g/dL, Serum Haptoglobin: 110 mg/dL (Normal). LDH: 185 U/L. No evidence of autoimmune hemolytic anemia in peripheral blood."
    ],
    "Diabetes": [
        "DIABETIC METABOLIC PANEL. Patient: John Smith. Fasting Blood Glucose (FBG): 182 mg/dL (Ref: 70 - 99 mg/dL, High). Postprandial Blood Sugar (PPBS 2-hour): 264 mg/dL (Ref: < 140 mg/dL, High). Glycated Hemoglobin (HbA1c): 9.4% (Ref: < 5.7%, High, indicates poorly controlled Type 2 Diabetes Mellitus). Estimated Average Glucose (eAG): 223 mg/dL. Urine Glucose: 2+ (Positive). Urine Ketones: Negative.",
        "ENDOCRINOLOGY EVALUATION: DIABETES MONITORING. Fasting Plasma Glucose: 134 mg/dL. HbA1c: 7.8% (Target < 7.0%). Fasting Serum C-Peptide: 3.1 ng/mL (Ref: 1.1 - 4.4). Fasting Serum Insulin: 18.5 uIU/mL (Elevated, insulin resistance). HOMA-IR: 6.1 (Significant insulin resistance). Lipid triad shows elevated triglycerides and low HDL cholesterol in diabetic patient.",
        "ORAL GLUCOSE TOLERANCE TEST (OGTT - 75g). Baseline Fasting Glucose: 118 mg/dL (Impaired Fasting Glucose). 1-Hour Post-load Glucose: 215 mg/dL. 2-Hour Post-load Glucose: 202 mg/dL (Confirms Diabetes Mellitus criteria >= 200 mg/dL). HbA1c: 6.9%. Recommended lifestyle modifications and anti-diabetic medication initiation.",
        "DIABETIC NEPHROPATHY SCREENING & METABOLIC PANEL. Random Blood Sugar (RBS): 210 mg/dL. Glycated Hemoglobin (HbA1c): 8.2%. Urine Microalbumin: 68 mg/L. Urine Creatinine: 1.2 g/L. Urine Albumin-to-Creatinine Ratio (UACR): 56.6 mg/g (Microalbuminuria present). Glycemic control sub-optimal. Regular endocrinological follow-up advised.",
        "DIABETIC KETOACIDOSIS (DKA) EVALUATION. Blood Glucose on admission: 384 mg/dL. Serum Beta-hydroxybutyrate: 4.8 mmol/L (Significantly elevated). Urine Ketones: 3+ (Strongly positive). Arterial pH: 7.28, Serum Bicarbonate: 14 mEq/L, Anion Gap: 21 (High anion gap metabolic acidosis). HbA1c: 11.2%. Initiated intravenous insulin infusion and fluid rehydration.",
        "CONTINUOUS GLUCOSE MONITORING (CGM) 14-DAY SUMMARY. Time in Range (70-180 mg/dL): 54% (Target > 70%). Time Above Range (> 180 mg/dL): 42%. Time Below Range (< 70 mg/dL): 4%. Glucose Management Indicator (GMI / calculated HbA1c): 8.1%. Mean Glucose: 194 mg/dL. Glycemic Variability (CV): 38.5%. Patient on basal-bolus insulin regimen.",
        "ANNUAL DIABETIC HEALTH CHECKUP. Fasting Plasma Glucose: 106 mg/dL (Pre-diabetes / Impaired fasting glucose). 2-Hour Post-Meal Glucose: 152 mg/dL. HbA1c: 5.9% (Pre-diabetic range 5.7 - 6.4%). Fasting Insulin: 12.0 uIU/mL. Lifestyle interventions including low glycemic index diet and daily exercise recommended.",
        "DIABETES PROFILE - TYPE 1 AUTOIMMUNE MARKERS. Anti-GAD Antibodies (Glutamic Acid Decarboxylase): 45.2 IU/mL (Positive > 5.0). Anti-Islet Cell Antibodies (ICA): Positive. Fasting C-Peptide: 0.3 ng/mL (Low, severe beta-cell secretory defect). Blood Glucose: 245 mg/dL, HbA1c: 10.1%. Findings consistent with autoimmune Type 1 Diabetes Mellitus.",
        "METABOLIC SYNDROME & GLYCEMIC PROFILE. Fasting Blood Glucose: 142 mg/dL. Postprandial Blood Glucose: 198 mg/dL. Glycated Hemoglobin: 7.4%. Serum Fructose-amine: 340 umol/L. Patient has established Type 2 Diabetes on Metformin and SGLT2 inhibitor therapy.",
        "OUTPATIENT ENDOCRINE LAB REPORT. HbA1c test result: 6.4%. Estimated average glucose: 137 mg/dL. Fasting blood sugar: 112 mg/dL. Urine dipstick for ketones: negative, protein: negative, glucose: trace. Adequate glycemic control on current oral hypoglycemic regimen."
    ],
    "Cardiology": [
        "12-LEAD ELECTROCARDIOGRAM (ECG) REPORT. Rhythm: Normal Sinus Rhythm. Heart Rate: 78 bpm. PR Interval: 160 ms. QRS Duration: 88 ms. QT/QTc Interval: 390/422 ms. P wave axis: 52 deg, QRS axis: 45 deg. ST-T Segment Analysis: No acute ST elevation or depression. T waves upright across precordial leads. Impression: Normal electrocardiogram without evidence of acute ischemia or arrhythmia.",
        "ECHOCARDIOGRAPHY (2D ECHO WITH DOPPLER) REPORT. Left Ventricular Ejection Fraction (LVEF): 55-60% (Normal systolic function). Left ventricular internal dimension in diastole (LVIDd): 4.8 cm, systole (LVIDs): 3.1 cm. Interventricular septum: 1.1 cm. Left atrium mildly dilated (3.9 cm). Mitral valve shows mild regurgitation. Aortic valve trileaflet with normal excursion, no stenosis. No pericardial effusion. Diastolic dysfunction Grade 1 (impaired relaxation).",
        "CARDIAC BIOMARKERS / ACUTE CORONARY SYNDROME PANEL. High-Sensitivity Cardiac Troponin I (hs-cTnI): 845.2 ng/L (Ref: < 14.0 ng/L, Critical High). Creatine Kinase-MB (CK-MB): 34.6 ng/mL (Ref: < 5.0 ng/mL). Total CK: 420 U/L. Myoglobin: 165 ng/mL. Clinical correlation: Findings highly indicative of acute myocardial infarction (NSTEMI). Emergency cardiology evaluation recommended.",
        "CARDIAC CATHETERIZATION & CORONARY ANGIOGRAPHY REPORT. Access: Right radial artery. Findings: Left Main Coronary Artery (LMCA) is patent without significant stenosis. Left Anterior Descending (LAD) artery shows 85% proximal tubular stenosis with TIMI 2 flow. Left Circumflex (LCx) artery shows diffuse 40% mid-vessel disease. Right Coronary Artery (RCA) is dominant with 70% ostial stenosis. Successful drug-eluting stent (DES) placement to LAD with TIMI 3 flow restored.",
        "24-HOUR HOLTER MONITORING REPORT. Total beats recorded: 104,210. Average heart rate: 72 bpm, Minimum HR: 48 bpm (during sleep), Maximum HR: 132 bpm. Underlying rhythm: Sinus rhythm. Ventricular ectopy: 42 isolated premature ventricular contractions (PVCs), no couplets or ventricular tachycardia. Supraventricular ectopy: 18 PACs. Patient diary: Brief palpitation corresponded to sinus tachycardia. No pauses > 2.0 seconds.",
        "TREADMILL STRESS TEST (TMT) - BRUCE PROTOCOL. Total exercise time: 8 minutes 45 seconds (Target heart rate 85% achieved at 148 bpm). Resting BP: 124/80 mmHg, Peak BP: 172/90 mmHg. Electrocardiographic response: 1.8 mm horizontal ST-segment depression in leads V4-V6 during Stage 3, persisting 4 minutes into recovery. Impression: Positive stress test for inducible myocardial ischemia at moderate workload.",
        "HEART FAILURE WORKUP - NT-PROBNP LAB REPORT. N-Terminal Pro B-Type Natriuretic Peptide (NT-proBNP): 3,420 pg/mL (Ref: < 125 pg/mL, Significantly elevated). Clinical presentation: NYHA Class III dyspnea on exertion and lower extremity edema. Transthoracic echocardiogram confirms reduced ejection fraction (HFrEF) with LVEF 32% and global left ventricular hypokinesis.",
        "CARDIAC ELECTROPHYSIOLOGY CONSULTATION. Indication: Paroxysmal Supraventricular Tachycardia (PSVT). Baseline ECG demonstrates short PR interval (108 ms) and delta wave in lead II, III, aVF and V4-V6 consistent with Wolff-Parkinson-White (WPW) pattern. Radiofrequency catheter ablation of right posteroseptal accessory pathway performed successfully.",
        "TRANSESOPHAGEAL ECHOCARDIOGRAM (TEE). Indication: Evaluation of bacteremia and potential infective endocarditis. Findings: Left ventricular systolic function preserved. Aortic valve: severe fibrocalcific changes with moderate aortic regurgitation. No mobile vegetations identified on aortic, mitral, or tricuspid leaflets. Left atrial appendage is free of thrombus; LAA emptying velocity 52 cm/s.",
        "CARDIAC MRI REPORT WITH DELAYED ENHANCEMENT. Cine imaging shows left ventricular end-diastolic volume index of 88 mL/m2, LVEF 52%. T1 mapping reveals diffuse interstitial fibrosis. Late gadolinium enhancement (LGE) reveals patchy mid-myocardial hyperenhancement in basal to mid inferolateral wall, sparing subendocardium, indicative of non-ischemic cardiomyopathy / prior myocarditis."
    ],
    "Radiology": [
        "CHEST RADIOGRAPH (X-RAY) PA VIEW. Clinical History: Cough, fever, and right-sided pleuritic chest pain. Findings: The heart size is within normal limits with cardiothoracic ratio < 0.5. Trachea is central. There is a dense, patchy alveolar consolidation in the right middle and lower lobes with air bronchograms. Right costophrenic angle is blunted, suggesting mild reactive pleural effusion. Left lung field is clear. Bony thorax and soft tissues unremarkable. Impression: Right middle and lower lobe pneumonia with associated parapneumonic effusion.",
        "HIGH RESOLUTION COMPUTED TOMOGRAPHY (HRCT) OF THORAX. Technique: Thin axial volumetric CT sections of chest without intravenous contrast. Findings: Bilateral peripheral and subpleural ground-glass opacities (GGO) noted involving posterior segments of lower lobes. Interlobular septal thickening producing a 'crazy-paving' pattern in localized areas. No pulmonary masses, cavitation, or pneumothorax. Mediastinal and hilar lymph nodes within normal limits. Impression: Interstitial lung disease / viral pneumonitis pattern.",
        "MAGNETIC RESONANCE IMAGING (MRI) OF BRAIN. Sequences: Axial T1, T2, FLAIR, DWI, ADC, and Sagittal T1. Clinical indication: Chronic headache and left-sided numbness. Findings: Ventricular system and cortical sulci appear normal for age. No midline shift or mass effect. Multiple discrete focal hyperintensities on T2/FLAIR images in the periventricular and subcortical white matter, non-enhancing, without restricted diffusion on DWI. Compatible with mild chronic small vessel microvascular ischemic disease. Major intracranial flow voids preserved.",
        "ULTRASOUND (USG) EXAMINATION OF WHOLE ABDOMEN AND PELVIS. Liver: Normal size (13.8 cm) with smooth margins and homogeneous echotexture. No focal lesion. Gallbladder: Well distended, wall thickness normal (2.2 mm), lumen clear without calculus. Spleen: Normal size (9.5 cm). Pancreas: Visualized portions unremarkable. Kidneys: Both kidneys normal in size, shape, and cortical echogenicity. Corticomedullary differentiation preserved. No hydronephrosis or renal calculi. Urinary bladder: Normal wall thickness, pre-void volume 320 mL, post-void residual 20 mL. Impression: Normal abdominal ultrasound study.",
        "CONTRAST-ENHANCED COMPUTED TOMOGRAPHY (CECT) OF ABDOMEN. Examination: Multiphase helical CT of abdomen and pelvis following oral and IV contrast. Findings: Spleen, pancreas, adrenal glands are normal. Cecum and ascending colon show normal wall thickness. Terminal ileum demonstrates mural thickening with mucosal hyperenhancement and surrounding mesenteric fat stranding ('comb sign'), suggestive of active ileitis / inflammatory bowel disease. No evidence of bowel obstruction, perforation, or intra-abdominal abscess.",
        "DIGITAL RADIOGRAPHY - LUMBAR SPINE AP AND LATERAL VIEWS. Clinical history: Chronic low back pain with radiculopathy. Findings: Vertebral body heights and alignment are maintained. Disc space narrowing noted at L4-L5 and L5-S1 levels with marginal osteophyte formation and endplate sclerosis. Facet joint arthrosis present at lower lumbar levels. Posterior elements intact. Psoas muscle shadows preserved. Impression: Spondylosis of lumbar spine with multi-level degenerative disc disease at L4-L5 and L5-S1.",
        "CT SCAN OF THE HEAD / BRAIN (NON-CONTRAST). Indication: Fall with minor head trauma, acute confusion. Findings: No acute intracranial hemorrhage, subdural hematoma, epidural hematoma, or subarachnoid hemorrhage. No evidence of acute territorial cortical infarction. Basal cisterns and ventricles are symmetric without hydrocephalus. Calvarium and base of skull intact without fracture. Paranasal sinuses and mastoid air cells clear. Impression: No acute intracranial abnormality detected.",
        "MAMMOGRAPHY AND BREAST ULTRASOUND REPORT. Bilateral full-field digital mammography with tomosynthesis. Breast parenchymal density: Category B - scattered fibroglandular densities. Right breast: No dominant mass, suspicious microcalcifications, or architectural distortion. Left breast: A circumscribed, oval, hypoechoic mass measuring 1.2 x 0.8 cm at 2 o'clock, 4 cm from the nipple, with parallel orientation and posterior acoustic enhancement on ultrasound. Features classic for benign fibroadenoma. Assessment: BI-RADS Category 2 (Benign).",
        "DOPPLER ULTRASOUND OF LOWER EXTREMITY DEEP VEINS. Examination: Duplex ultrasonography of right lower extremity venous system. Findings: Common femoral, deep femoral, femoral, and popliteal veins are widely patent, fully compressible, with normal phasicity and augmentation. No intraluminal thrombus or color Doppler flow void. Posterior tibial and peroneal veins are unremarkable. Impression: Negative for deep vein thrombosis (DVT) in the right lower extremity.",
        "X-RAY CERVICAL SPINE AP, LATERAL AND FLEXION-EXTENSION. Findings: Normal cervical lordosis is preserved. No subluxation or fracture seen. Prevertebral soft tissue thickness normal. Minimal anterior osteophytes at C5-C6 with mild disc space narrowing. Neural foramina are patent bilaterally. Dynamic flexion and extension views show no signs of ligamentous instability. Impression: Mild cervical spondylosis."
    ],
    "Kidney": [
        "RENAL FUNCTION TEST (RFT / KFT) REPORT. Patient: Robert Taylor. Serum Creatinine: 2.85 mg/dL (Ref: 0.7 - 1.3 mg/dL, High). Blood Urea Nitrogen (BUN): 48 mg/dL (Ref: 7 - 20 mg/dL, High). Serum Urea: 102 mg/dL. Estimated Glomerular Filtration Rate (eGFR - CKD-EPI): 24 mL/min/1.73m2 (Ref: > 90, indicates severely decreased kidney function, Stage 4 Chronic Kidney Disease). Serum Uric Acid: 8.6 mg/dL (High). Serum Electrolytes: Sodium 138 mmol/L, Potassium 5.2 mmol/L (Mild hyperkalemia), Chloride 102 mmol/L, Bicarbonate 18 mmol/L.",
        "NEPHROLOGY CLINICAL PANEL: URINE ALBUMIN & RENAL CLEARANCE. 24-Hour Urine Protein: 1.85 g/24 hours (Ref: < 0.15 g/24 hr, Marked Proteinuria). 24-Hour Urine Creatinine: 1.1 g/day. Creatinine Clearance: 28 mL/min. Urine Albumin-to-Creatinine Ratio (UACR): 1,240 mg/g (Severely increased albuminuria, nephrotic range tendency). Serum Creatinine: 2.1 mg/dL, BUN: 38 mg/dL. Impression: Chronic kidney disease with significant proteinuria and renal impairment.",
        "URINE ROUTINE AND MICROSCOPIC EXAMINATION (URINALYSIS). Color: Pale yellow, Appearance: Turbid. Specific Gravity: 1.012, pH: 5.5. Protein / Albumin: 2+ (Positive), Glucose: Nil, Ketones: Nil. Microscopic examination: Pus cells (Leukocytes): 15-20 /HPF, Red Blood Cells (RBCs): 25-30 /HPF (Dysmorphic red cells present). Granular casts: 3-5 /LPF. Red cell casts: 1-2 /LPF. Renal epithelial cells: 2-4 /HPF. Clinical significance: Active urinary sediment with glomerulonephritis picture.",
        "RENAL ULTRASONOGRAPHY & DOPPLER REPORT. Right kidney measures 8.4 x 3.8 cm; Left kidney measures 8.6 x 3.9 cm (Bilateral small, shrunken kidneys). Diffuse thinning of renal parenchyma with cortical thickness reduced to 7 mm. Bilateral increased renal cortical echogenicity (Grade II-III), hyperechoic relative to liver parenchyma, with poor corticomedullary differentiation. No hydronephrosis, calculus, or perinephric collection. Impression: Features consistent with bilateral medical renal disease / end-stage renal disease (ESRD).",
        "KIDNEY STONE / NEPHROLITHIASIS EVALUATION. Serum Creatinine: 1.4 mg/dL. BUN: 22 mg/dL. Non-contrast CT KUB demonstrates a 6.5 mm radiopaque calculus lodged at the right proximal ureter with associated moderate right hydroureteronephrosis and perinephric stranding. Left kidney contains two non-obstructing calyceal microliths measuring 3 mm. Urinalysis shows microscopic hematuria with 40-50 RBCs/HPF.",
        "ACUTE KIDNEY INJURY (AKI) ASSESSMENT REPORT. Baseline Serum Creatinine: 0.9 mg/dL. Current Serum Creatinine: 3.4 mg/dL (Tripling of baseline value within 48 hours). BUN: 62 mg/dL. Urine output: Oliguria with < 0.5 mL/kg/h for 12 hours. Fractional Excretion of Sodium (FeNa): 0.6% (Consistent with pre-renal azotemia responding to intravenous fluid challenge). Urinalysis shows hyaline casts without active cellular sediment.",
        "RENAL BIOPSY PATHOLOGY REPORT. Light microscopy: 16 glomeruli evaluated. 3 globally sclerosed. Remaining glomeruli demonstrate diffuse mesangial hypercellularity and marked expansion of mesangial matrix. Immunofluorescence microscopy reveals intense granular mesangial staining for IgA (3+) and C3 (2+). Tubulointerstitial fibrosis involves approximately 20% of the cortex. Diagnosis: IgA Nephropathy (Berger's Disease), Oxford Classification M1, E0, S1, T0, C0.",
        "METABOLIC RENAL PANEL - ELECTROLYTES & MINERAL BONE DISEASE. Serum Creatinine: 4.1 mg/dL, eGFR: 14 mL/min/1.73m2 (CKD Stage 5). Serum Calcium: 8.1 mg/dL (Low), Serum Phosphorus: 6.4 mg/dL (High, hyperphosphatemia). Intact Parathyroid Hormone (iPTH): 340 pg/mL (Secondary hyperparathyroidism). Serum Bicarbonate: 16 mmol/L (Metabolic acidosis). Dialysis access planning discussed with patient.",
        "KIDNEY TRANSPLANT RECIPIENT SURVEILLANCE REPORT. Post-renal allograft ultrasound: Normal allograft perfusion with resistive index (RI) 0.64 in arcuate arteries. Serum Creatinine: 1.15 mg/dL (Stable). BUN: 18 mg/dL. Tacrolimus 12-hour trough level: 6.8 ng/mL (Target therapeutic window 5-8 ng/mL). Urine protein-to-creatinine ratio: 0.12 mg/mg (Normal). No sign of acute allograft rejection.",
        "POLYCYSTIC KIDNEY DISEASE (ADPKD) FOLLOW-UP. Clinical diagnosis: Autosomal Dominant Polycystic Kidney Disease. Serum Creatinine: 1.9 mg/dL, eGFR: 39 mL/min. Renal ultrasound confirms markedly enlarged kidneys bilaterally (Right 16.2 cm, Left 17.0 cm) containing innumerable cortical and medullary cysts of variable dimensions, some with internal echoes indicating previous cyst hemorrhage. Blood pressure controlled at 122/78 mmHg."
    ],
    "Liver": [
        "LIVER FUNCTION TEST (LFT) PANEL. Patient: Michael Brown. Total Bilirubin: 3.4 mg/dL (Ref: 0.2 - 1.2 mg/dL, High). Direct (Conjugated) Bilirubin: 2.1 mg/dL (Ref: 0.0 - 0.3 mg/dL, High). Indirect Bilirubin: 1.3 mg/dL. Alanine Aminotransferase (ALT / SGPT): 245 U/L (Ref: 7 - 56 U/L, Significantly High). Aspartate Aminotransferase (AST / SGOT): 198 U/L (Ref: 10 - 40 U/L, High). Alkaline Phosphatase (ALP): 185 U/L (Ref: 44 - 147 U/L). Gamma-Glutamyl Transferase (GGT): 140 U/L. Total Protein: 6.8 g/dL, Albumin: 3.2 g/dL, Globulin: 3.6 g/dL, A/G Ratio: 0.89. Impression: Acute hepatocellular injury with cholestatic jaundice.",
        "HEPATOLOGY WORKUP - CIRRHOSIS & HEPATIC FIBROSIS. Total Serum Bilirubin: 2.8 mg/dL. Serum Albumin: 2.6 g/dL (Hypoalbuminemia). Prothrombin Time (PT): 18.2 seconds, INR: 1.62 (Impaired hepatic synthetic function). AST: 84 U/L, ALT: 56 U/L (AST/ALT ratio > 1.5, typical of advanced fibrosis/cirrhosis). Platelet count: 88,000 /uL (Splenomegaly/hypersplenism). Child-Pugh Score: 9 (Class B). Meld-Na Score: 18. Abdominal sonography confirms nodular liver surface with coarsened echotexture and moderate ascites.",
        "NON-ALCOHOLIC FATTY LIVER DISEASE (NAFLD / NASH) REPORT. Ultrasound Whole Abdomen reveals diffusely increased echogenicity of the liver parenchyma ('bright liver') with deep attenuation of ultrasound beam and impaired visualization of intrahepatic vessels. Grade II hepatic steatosis. Serum ALT: 72 U/L, AST: 58 U/L, GGT: 82 U/L. Total Bilirubin: 0.9 mg/dL. FIB-4 Index: 1.94 (Intermediate risk for advanced liver fibrosis). Diet and lifestyle counseling initiated.",
        "VIRAL HEPATITIS SEROLOGY & MOLECULAR QUANTITATION. Hepatitis B Surface Antigen (HBsAg): Reactive / Positive. Hepatitis B e Antigen (HBeAg): Positive. Anti-HBs: Non-reactive. HBV DNA Quantitative PCR: 4,500,000 IU/mL (High viral replication). ALT: 115 U/L, AST: 88 U/L. Serum Bilirubin: 1.4 mg/dL. Anti-HCV: Negative. Diagnosis: Chronic active Hepatitis B infection. Antiviral therapy indicated.",
        "CHOLESTATIC LIVER DISEASE & BILIARY INVESTIGATION. Serum Alkaline Phosphatase (ALP): 480 U/L (Markedly elevated). Gamma-Glutamyl Transferase (GGT): 360 U/L. Total Bilirubin: 4.8 mg/dL with Direct Bilirubin 3.9 mg/dL. ALT: 62 U/L, AST: 55 U/L. Anti-Mitochondrial Antibodies (AMA - M2): Strongly Positive (Titre 1:160). Serum IgM: 380 mg/dL (Elevated). Impression: Primary Biliary Cholangitis (PBC).",
        "ACUTE HEPATITIS EVALUATION. Patient presenting with jaundice, dark urine, and right upper quadrant abdominal tenderness. Hepatitis A IgM (Anti-HAV IgM): Positive. Hepatitis E IgM: Negative. HBsAg: Negative. Anti-HCV: Negative. ALT: 1,840 U/L (Marked transaminitis), AST: 1,420 U/L. Total Bilirubin: 7.2 mg/dL, Direct Bilirubin: 5.1 mg/dL. INR: 1.15. Consistent with acute viral Hepatitis A.",
        "LIVER FIBROSCAN (TRANSIENT ELASTOGRAPHY) REPORT. Median Liver Stiffness Measurement (LSM): 14.8 kPa (Interquartile range IQR 1.2 kPa, IQR/med 8%). Controlled Attenuation Parameter (CAP): 315 dB/m. Interpretation: LSM corresponds to Metavir Stage F4 (Established liver cirrhosis). CAP indicates severe Grade 3 hepatic steatosis. Regular surveillance for hepatocellular carcinoma with AFP and ultrasound advised.",
        "ALCOHOLIC HEPATITIS CLINICAL ASSESSMENT. Patient with history of heavy ethanol consumption. AST: 310 U/L, ALT: 118 U/L (Characteristic AST/ALT ratio > 2.0). GGT: 520 U/L (Marked elevation). Total Bilirubin: 9.6 mg/dL. Prothrombin Time: 21.0 seconds, INR: 1.95. Maddrey's Discriminant Function (DF): 41.2 (Severe alcoholic hepatitis, DF > 32). Serum Albumin: 2.4 g/dL. Leukocytosis with WBC 15,200 /uL.",
        "HEPATOCELLULAR CARCINOMA (HCC) SURVEILLANCE & TUMOR MARKER. Serum Alpha-Fetoprotein (AFP): 480 ng/mL (Ref: < 8.0 ng/mL, Markedly elevated). Serum Des-gamma-carboxy prothrombin (DCP / PIVKA-II): 120 mAU/mL. Triphasic CT Liver confirms a 3.2 cm hypervascular lesion in Segment VI with arterial phase enhancement and delayed venous washout (LI-RADS 5 - definitely HCC) on background of cirrhotic liver.",
        "POST-CHOLECYSTECTOMY BILIARY PROFILE. Total Bilirubin: 1.1 mg/dL (Normal). Direct Bilirubin: 0.3 mg/dL. Serum ALT: 32 U/L, AST: 28 U/L. ALP: 95 U/L, GGT: 34 U/L. Total Protein: 7.2 g/dL, Albumin: 4.3 g/dL. Normalized hepatic enzyme profile following resolution of choledocholithiasis."
    ]
}

# Generate expanded dataset with variations
rows = []
for category, samples in categories.items():
    for text in samples:
        rows.append((text, category))

# Add templated variations to reach 240+ rich clinical reports
lab_names = [
    "Metro Health Laboratories", "Apex Diagnostics & Research", "CareWell Pathology Services",
    "City Central Hospital Lab", "BioQuest Clinical Laboratories", "St. Jude Memorial Diagnostics",
    "Premier Diagnostic Center", "Horizon Clinical Pathology"
]

doctors = [
    "Dr. Arvind Sharma, MD", "Dr. Sarah Jenkins, MD, FACP", "Dr. Rajesh Gupta, MD (Medicine)",
    "Dr. Elizabeth Vance, MD", "Dr. K. S. Raman, DNB", "Dr. Marcus Reed, MD, FACC"
]

def make_variations():
    variations = []
    
    # Blood Test variations
    for i in range(30):
        hb = round(random.uniform(7.5, 16.5), 1)
        wbc = random.randint(3500, 15000)
        plt = random.randint(80, 450) * 1000
        mcv = round(random.uniform(68.0, 102.0), 1)
        mch = round(random.uniform(21.0, 34.0), 1)
        esr = random.randint(5, 65)
        neut = random.randint(45, 82)
        lymph = 100 - neut - random.randint(2, 8)
        lab = random.choice(lab_names)
        doc = random.choice(doctors)
        
        sample = (
            f"{lab} - CLINICAL HEMATOLOGY REPORT. Referred by: {doc}. "
            f"TEST NAME: COMPLETE BLOOD COUNT (CBC). Hemoglobin (Hb): {hb} g/dL. "
            f"RBC Count: {round(hb/3.2, 2)} mil/uL. PCV / Hematocrit: {round(hb*3.1, 1)}%. "
            f"Mean Corpuscular Volume (MCV): {mcv} fL. MCH: {mch} pg. MCHC: 32.8 g/dL. "
            f"Total White Blood Cell Count (WBC): {wbc} /mcL. "
            f"Differential Leukocyte Count: Neutrophils {neut}%, Lymphocytes {lymph}%, "
            f"Monocytes 4%, Eosinophils 3%, Basophils 1%. "
            f"Platelet Count: {plt} /mcL. ESR (Westergren method): {esr} mm/hr. "
            f"Peripheral Blood Smear Examination: Red blood cell morphology evaluated. "
            f"Impression: Hemogram parameters tabulated above."
        )
        variations.append((sample, "Blood Test"))

    # Diabetes variations
    for i in range(30):
        fbg = random.randint(95, 290)
        ppbs = random.randint(130, 380)
        hba1c = round(random.uniform(5.4, 12.8), 1)
        lab = random.choice(lab_names)
        doc = random.choice(doctors)
        status = "Good glycemic control" if hba1c < 7.0 else "Poorly controlled hyperglycemia"
        
        sample = (
            f"{lab} - DIABETES CARE & METABOLIC INVESTIGATION. Consulting Physician: {doc}. "
            f"Fasting Plasma Glucose (FBS): {fbg} mg/dL (Reference: 70-100 mg/dL). "
            f"Post-Prandial Plasma Glucose (PPBS 2 hrs post meal): {ppbs} mg/dL (Reference: < 140 mg/dL). "
            f"Glycated Hemoglobin (HbA1c): {hba1c}% (Standard NGSP/IFCC certified). "
            f"Estimated Average Glucose (eAG): {round(28.7 * hba1c - 46.7, 1)} mg/dL. "
            f"Urine Glucose: {'Negative' if fbg < 180 else '2+ (Positive)'}. Urine Ketone bodies: Negative. "
            f"Clinical Remarks: {status}. Consistent with Type 2 Diabetes Mellitus evaluation. "
            f"Advised continuation of diabetic diet plan and clinical correlation."
        )
        variations.append((sample, "Diabetes"))

    # Cardiology variations
    for i in range(30):
        hr = random.randint(55, 115)
        lvef = random.randint(30, 65)
        trop = round(random.uniform(5.0, 950.0), 1)
        lab = random.choice(lab_names)
        doc = random.choice(doctors)
        
        sample = (
            f"{lab} - CARDIAC DIAGNOSTIC REPORT & ECHOCARDIOGRAM. Cardiologist: {doc}. "
            f"Resting 12-Lead Electrocardiogram (ECG): Heart rate: {hr} bpm. Sinus rhythm. "
            f"PR interval: 154 ms. QRS duration: 84 ms. QTc: 418 ms. Axis: Normal. "
            f"2D Echocardiogram Study: Left Ventricular Ejection Fraction (LVEF): {lvef}%. "
            f"Interventricular septum thickness: 1.0 cm. Posterior wall thickness: 0.9 cm. "
            f"Valvular assessment: Aortic, mitral, and tricuspid valve leaflets inspected. "
            f"Cardiac Biomarkers: Serum High-Sensitivity Troponin I: {trop} pg/mL (Cut-off: 14 pg/mL). "
            f"CK-MB mass: {round(trop/25 + 2.0, 1)} ng/mL. "
            f"Impression: Cardiovascular assessment showing LVEF {lvef}%, coronary risk stratification documented."
        )
        variations.append((sample, "Cardiology"))

    # Radiology variations
    for i in range(30):
        modalities = [
            ("CHEST RADIOGRAPH (X-RAY PA VIEW)", "Lungs are clear of active infiltration or consolidation. Costophrenic angles sharp. Cardiothoracic ratio normal."),
            ("CT SCAN OF BRAIN (NON-CONTRAST)", "Cerebral parenchyma demonstrates normal attenuation. No intracranial hemorrhage or acute territorial stroke. Ventricles normal."),
            ("ULTRASOUND WHOLE ABDOMEN", "Liver normal in size and echotexture. Gallbladder calculi absent. Common bile duct normal. Spleen and pancreas unremarkable."),
            ("MRI CERVICAL / LUMBAR SPINE", "Spinal cord normal caliber and signal intensity. Mild intervertebral disc degeneration at L4-L5 with annular bulge. No cord compression."),
            ("HIGH RESOLUTION CT CHEST (HRCT)", "No architectural distortion or honeycombing. Clear bronchovascular bundles. Pleural spaces unremarkable. Normal pulmonary CT study.")
        ]
        mod, findings = random.choice(modalities)
        lab = random.choice(lab_names)
        doc = random.choice(doctors)
        
        sample = (
            f"{lab} - DEPARTMENT OF RADIOLOGY AND MEDICAL IMAGING. Radiologist: {doc}. "
            f"PROCEDURE: {mod}. "
            f"TECHNIQUE: Standard multi-projection digital radiographic / cross-sectional imaging protocol. "
            f"FINDINGS: {findings} Soft tissue margins and bony structures demonstrate normal density. "
            f"No radiopaque foreign body or suspicious focal mass identified. "
            f"IMPRESSION: Radiological examination completed as reported above. Diagnostic report signed by Consultant Radiologist."
        )
        variations.append((sample, "Radiology"))

    # Kidney variations
    for i in range(30):
        creat = round(random.uniform(0.7, 5.8), 2)
        bun = random.randint(12, 85)
        egfr = max(8, int(175 * (creat ** -1.154) * (random.choice([0.742, 1.0]))))
        uric = round(random.uniform(4.0, 10.5), 1)
        lab = random.choice(lab_names)
        doc = random.choice(doctors)
        
        sample = (
            f"{lab} - RENAL PROFILE & NEPHROLOGY INVESTIGATION. Attending Physician: {doc}. "
            f"KIDNEY FUNCTION TEST (KFT / RFT): "
            f"Serum Creatinine: {creat} mg/dL (Reference Range: 0.60 - 1.20 mg/dL). "
            f"Blood Urea Nitrogen (BUN): {bun} mg/dL (Reference Range: 7 - 20 mg/dL). "
            f"Estimated Glomerular Filtration Rate (eGFR): {egfr} mL/min/1.73m2. "
            f"Serum Uric Acid: {uric} mg/dL. Serum Sodium: 139 mEq/L, Potassium: {round(random.uniform(3.8, 5.8), 1)} mEq/L. "
            f"Urinalysis Routine: Urine Protein: {'Trace / Negative' if creat < 1.3 else '2+ Positive'}. "
            f"Pus Cells: 2-3 /HPF, Red Blood Cells: 1-2 /HPF. "
            f"Impression: Renal biochemistry panel displaying eGFR of {egfr} mL/min/1.73m2. Clinical nephrology evaluation indicated."
        )
        variations.append((sample, "Kidney"))

    # Liver variations
    for i in range(30):
        bili = round(random.uniform(0.6, 6.5), 1)
        alt = random.randint(22, 290)
        ast = random.randint(20, 240)
        alp = random.randint(65, 320)
        ggt = random.randint(25, 210)
        alb = round(random.uniform(2.5, 4.6), 1)
        lab = random.choice(lab_names)
        doc = random.choice(doctors)
        
        sample = (
            f"{lab} - HEPATIC FUNCTION & LIVER PANEL (LFT). Consultant: {doc}. "
            f"Total Bilirubin: {bili} mg/dL (Ref: 0.2 - 1.2 mg/dL). "
            f"Direct Bilirubin: {round(bili*0.6, 1)} mg/dL. Indirect Bilirubin: {round(bili*0.4, 1)} mg/dL. "
            f"SGPT / ALT (Alanine Aminotransferase): {alt} U/L (Ref: < 45 U/L). "
            f"SGOT / AST (Aspartate Aminotransferase): {ast} U/L (Ref: < 40 U/L). "
            f"Alkaline Phosphatase (ALP): {alp} U/L. Gamma-Glutamyl Transferase (GGT): {ggt} U/L. "
            f"Total Serum Protein: 7.0 g/dL, Serum Albumin: {alb} g/dL, Serum Globulin: {round(7.0 - alb, 1)} g/dL. "
            f"Albumin/Globulin (A/G) Ratio: {round(alb / (7.0 - alb), 2)}. "
            f"Impression: Hepatic biochemistry profiling with transaminase and cholestatic enzyme assessment as recorded."
        )
        variations.append((sample, "Liver"))

    return variations

all_data = rows + make_variations()
random.seed(42)
random.shuffle(all_data)

os.makedirs(os.path.dirname(DATASET_PATH), exist_ok=True)
with open(DATASET_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "category"])
    for text, cat in all_data:
        writer.writerow([text, cat])

print(f"Generated {len(all_data)} medical reports in {DATASET_PATH}")
from collections import Counter
counts = Counter([cat for _, cat in all_data])
for cat, count in counts.items():
    print(f"  - {cat}: {count} reports")
