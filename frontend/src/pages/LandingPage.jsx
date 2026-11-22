import React from 'react';
import { NavLink } from 'react-router-dom';
import PublicNavbar from '../layouts/PublicNavbar';
import PublicFooter from '../layouts/PublicFooter';
import {
  Activity,
  ArrowRight,
  FileCheck2,
  ScanText,
  BrainCircuit,
  Lock,
  Download,
  CheckCircle2,
  Droplet,
  HeartPulse,
  Syringe,
  Layers,
  Sparkles,
  ShieldCheck,
  BarChart2
} from 'lucide-react';

const LandingPage = () => {
  const categories = [
    {
      name: 'Blood Test',
      icon: Droplet,
      color: 'text-rose-600 bg-rose-50 border-rose-200',
      badge: 'Hematology',
      desc: 'Complete blood count (CBC), hemoglobin, hematocrit, platelet counts, differential WBC, ESR, ferritin, and coagulation profile.',
      keywords: ['Hemoglobin', 'Platelets', 'WBC', 'MCV', 'Coagulation']
    },
    {
      name: 'Diabetes',
      icon: Syringe,
      color: 'text-amber-600 bg-amber-50 border-amber-200',
      badge: 'Endocrinology',
      desc: 'Fasting blood sugar, postprandial glucose, glycated hemoglobin (HbA1c), oral glucose tolerance tests, insulin, and ketones.',
      keywords: ['HbA1c', 'Fasting Blood Glucose', 'PPBS', 'C-Peptide', 'eAG']
    },
    {
      name: 'Cardiology',
      icon: HeartPulse,
      color: 'text-pink-600 bg-pink-50 border-pink-200',
      badge: 'Cardiovascular',
      desc: '12-lead electrocardiograms (ECG/EKG), 2D echocardiograms (LVEF), cardiac enzymes, Troponin I/T, CK-MB, and Holter monitoring.',
      keywords: ['ECG', 'LVEF', 'Troponin I', 'Sinus Rhythm', 'Echocardiogram']
    },
    {
      name: 'Radiology',
      icon: Layers,
      color: 'text-purple-600 bg-purple-50 border-purple-200',
      badge: 'Diagnostic Imaging',
      desc: 'Chest X-rays (CXR), CT scans of brain/chest/abdomen, MRI scans, ultrasound (USG) whole abdomen, and mammography reports.',
      keywords: ['Chest X-Ray', 'CT Scan', 'MRI Brain', 'Ultrasound', 'Consolidation']
    },
    {
      name: 'Kidney',
      icon: Activity,
      color: 'text-cyan-600 bg-cyan-50 border-cyan-200',
      badge: 'Nephrology',
      desc: 'Renal function tests (RFT/KFT), serum creatinine, blood urea nitrogen (BUN), eGFR, urinalysis, 24-hr urine protein, and renal stones.',
      keywords: ['Creatinine', 'BUN', 'eGFR', 'Proteinuria', 'Uric Acid']
    },
    {
      name: 'Liver',
      icon: Sparkles,
      color: 'text-emerald-600 bg-emerald-50 border-emerald-200',
      badge: 'Hepatology',
      desc: 'Liver function test (LFT), total/direct bilirubin, SGPT/ALT, SGOT/AST, ALP, GGT, serum albumin, and viral hepatitis markers.',
      keywords: ['Bilirubin', 'SGPT / ALT', 'SGOT / AST', 'Alkaline Phosphatase', 'Albumin']
    }
  ];

  const steps = [
    {
      step: '01',
      title: 'Upload Document',
      desc: 'Drop any medical document in PDF, PNG, JPG, or JPEG format. Our client verifies size, format, and legibility instantly.',
      icon: ScanText
    },
    {
      step: '02',
      title: 'Digital & OCR Extraction',
      desc: 'PyMuPDF parses native digital text; high-performance OCR deciphers scanned prints and high-resolution hospital lab camera captures.',
      icon: FileCheck2
    },
    {
      step: '03',
      title: 'NLP TF-IDF Classification',
      desc: 'Our trained multi-class machine learning model analyzes medical n-grams, biomarker patterns, and clinical phrasing to infer the exact specialty.',
      icon: BrainCircuit
    },
    {
      step: '04',
      title: 'Insights & Downloadable PDF',
      desc: 'Review predicted category, calibrated confidence scores, extracted clinical text preview, and generate an official audit-ready PDF summary.',
      icon: Download
    }
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <PublicNavbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 lg:pt-20 lg:pb-32 bg-radial from-sky-50 via-slate-50 to-white border-b border-slate-200/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Left Column: Headlines */}
            <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-sky-100/80 border border-sky-200 text-sky-800 text-xs font-semibold shadow-xs">
                <Sparkles className="w-4 h-4 text-sky-600" />
                <span>Next-Generation Document Intelligence</span>
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.15]">
                Smarter Medical Reports. <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-600 to-blue-600">
                  Organized by AI.
                </span>
              </h1>

              <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto lg:mx-0 leading-relaxed font-normal">
                MediScan AI automatically extracts text from clinical lab reports, scanned PDFs, and diagnostic images using OCR and NLP, classifying them into 6 specialized medical categories with calibrated confidence scores.
              </p>

              <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
                <NavLink
                  to="/register"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 rounded-xl bg-gradient-to-r from-sky-600 to-blue-600 text-white font-semibold shadow-md shadow-sky-600/25 hover:shadow-lg hover:from-sky-700 hover:to-blue-700 transition-all text-sm sm:text-base active:scale-[0.98]"
                >
                  <span>Get Started Free</span>
                  <ArrowRight className="w-4 h-4" />
                </NavLink>

                <NavLink
                  to="/login"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-white border border-slate-200 text-slate-700 font-semibold hover:bg-slate-50 transition-colors text-sm sm:text-base shadow-xs"
                >
                  <span>Sign In to Dashboard</span>
                </NavLink>
              </div>

              {/* Trust Indicators */}
              <div className="pt-6 border-t border-slate-200/80 grid grid-cols-3 gap-4 text-left">
                <div>
                  <p className="text-2xl font-bold text-slate-900">93.3%</p>
                  <p className="text-xs text-slate-500 font-medium">Evaluation Accuracy</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-slate-900">6</p>
                  <p className="text-xs text-slate-500 font-medium">Specialty Categories</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-slate-900">&lt; 1.5s</p>
                  <p className="text-xs text-slate-500 font-medium">Average Processing</p>
                </div>
              </div>
            </div>

            {/* Right Column: Visual Preview Card */}
            <div className="lg:col-span-5">
              <div className="relative mx-auto max-w-md bg-white rounded-2xl shadow-xl shadow-slate-200/60 border border-slate-200/80 p-6 space-y-5">
                <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-lg bg-sky-100 text-sky-700 flex items-center justify-center font-bold text-sm">
                      <ScanText className="w-5 h-5" />
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-800">Sample_CBC_LabReport.pdf</p>
                      <p className="text-[11px] text-slate-400">Extracted & Classified</p>
                    </div>
                  </div>
                  <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                    98.4% Confidence
                  </span>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/60 font-mono text-[11px] text-slate-600 space-y-1">
                  <p className="text-slate-400 text-[10px]"># OCR PARSED TEXT FRAGMENT:</p>
                  <p className="font-semibold text-slate-800">COMPLETE BLOOD COUNT (CBC)</p>
                  <p>Hemoglobin: 14.2 g/dL | WBC: 6,800 /uL</p>
                  <p>Platelet: 245,000 /mcL | MCV: 88.5 fL</p>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-xs font-semibold text-slate-700">
                    <span>Predicted Specialty</span>
                    <span className="text-rose-600 font-bold">Blood Test (Hematology)</span>
                  </div>
                  <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                    <div className="bg-gradient-to-r from-sky-500 to-rose-500 h-full rounded-full w-[98%]"></div>
                  </div>
                </div>

                <div className="pt-2 flex items-center justify-between text-xs text-slate-400">
                  <span className="flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Safe Server Hash
                  </span>
                  <span>PDF Export Ready</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs font-bold uppercase tracking-wider text-sky-600 mb-2">Core Capabilities</h2>
            <h3 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
              Built for Modern Clinical Workflows
            </h3>
            <p className="mt-3 text-slate-600 text-sm sm:text-base">
              A complete pipeline designed to process both searchable digital PDFs and physical camera-captured laboratory scans.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center mb-5">
                <ScanText className="w-6 h-6" />
              </div>
              <h4 className="text-base font-bold text-slate-900 mb-2">Dual OCR Engine</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                PyMuPDF for rapid digital text extraction, combined with an on-device OCR engine for scanned PDFs and PNG/JPG images.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center mb-5">
                <BrainCircuit className="w-6 h-6" />
              </div>
              <h4 className="text-base font-bold text-slate-900 mb-2">Calibrated NLP Model</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                TF-IDF bi-gram feature extraction paired with calibrated multinomial classification provides realistic confidence probabilities.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center mb-5">
                <Lock className="w-6 h-6" />
              </div>
              <h4 className="text-base font-bold text-slate-900 mb-2">User Isolation & Privacy</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Strict database isolation ensures users access only their own uploads. Secure filenames prevent directory traversal vulnerabilities.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80 hover:shadow-md transition-shadow">
              <div className="w-12 h-12 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center mb-5">
                <Download className="w-6 h-6" />
              </div>
              <h4 className="text-base font-bold text-slate-900 mb-2">PDF Report Generation</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Instant ReportLab generation of clean, professional summary certificates with disclaimer headers and extracted text previews.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-slate-50 border-y border-slate-200/70">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs font-bold uppercase tracking-wider text-sky-600 mb-2">End-to-End Workflow</h2>
            <h3 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
              From Raw File to Categorized Result
            </h3>
            <p className="mt-3 text-slate-600 text-sm sm:text-base">
              Four streamlined steps taking less than two seconds to index your documents.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {steps.map((st, i) => {
              const Icon = st.icon;
              return (
                <div key={i} className="relative p-6 rounded-2xl bg-white border border-slate-200/80 shadow-xs">
                  <span className="text-3xl font-black text-slate-200 absolute top-5 right-5">
                    {st.step}
                  </span>
                  <div className="w-11 h-11 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center mb-4">
                    <Icon className="w-5 h-5" />
                  </div>
                  <h4 className="text-base font-bold text-slate-900 mb-2">{st.title}</h4>
                  <p className="text-xs text-slate-500 leading-relaxed">{st.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Supported Categories Grid */}
      <section id="categories" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs font-bold uppercase tracking-wider text-sky-600 mb-2">Document Coverage</h2>
            <h3 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
              6 Specialized Medical Categories
            </h3>
            <p className="mt-3 text-slate-600 text-sm sm:text-base">
              Trained specifically on authentic clinical terminology, laboratory reference ranges, and diagnostic notes.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {categories.map((cat, idx) => {
              const Icon = cat.icon;
              return (
                <div
                  key={idx}
                  className="p-6 rounded-2xl bg-slate-50/70 border border-slate-200/80 hover:border-sky-300 hover:shadow-md transition-all group"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center border ${cat.color} group-hover:scale-105 transition-transform`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="text-[11px] font-semibold px-2.5 py-1 rounded-full bg-slate-200/60 text-slate-700">
                      {cat.badge}
                    </span>
                  </div>

                  <h4 className="text-lg font-bold text-slate-900 mb-2">{cat.name}</h4>
                  <p className="text-xs text-slate-600 leading-relaxed mb-4">{cat.desc}</p>

                  <div className="flex flex-wrap gap-1.5 pt-2 border-t border-slate-200/60">
                    {cat.keywords.map((kw, k) => (
                      <span key={k} className="text-[10px] font-medium px-2 py-0.5 rounded-md bg-white border border-slate-200 text-slate-600">
                        {kw}
                      </span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Medical Disclaimer Banner */}
      <section className="py-12 bg-amber-50/60 border-y border-amber-200/60">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 flex items-start gap-4">
          <ShieldCheck className="w-7 h-7 text-amber-600 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <h4 className="text-sm font-bold text-amber-900">Healthcare Disclaimer & Scope of Application</h4>
            <p className="text-xs text-amber-800 leading-relaxed">
              MediScan AI is strictly a medical document classification and indexing system for workflow organization. It does <strong>not</strong> perform diagnostic clinical evaluation, identify diseases, provide medical diagnoses, or prescribe treatment. For medical concerns, always consult a licensed doctor or healthcare professional.
            </p>
          </div>
        </div>
      </section>

      <PublicFooter />
    </div>
  );
};

export default LandingPage;
