import React from 'react';
import { Activity, ShieldAlert, Cpu, HeartPulse } from 'lucide-react';

const PublicFooter = () => {
  return (
    <footer className="bg-slate-900 text-slate-300 pt-16 pb-12 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-slate-800">
          {/* Brand */}
          <div className="md:col-span-1">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-9 h-9 rounded-xl bg-sky-500 flex items-center justify-center text-white shadow-md">
                <Activity className="w-5 h-5 stroke-[2.2]" />
              </div>
              <span className="font-bold text-xl text-white tracking-tight">MediScan AI</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Intelligent document classification and clinical report indexing using modern Natural Language Processing and OCR.
            </p>
          </div>

          {/* Quick links */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200 mb-4">Platform</h4>
            <ul className="space-y-2 text-xs text-slate-400">
              <li><a href="#features" className="hover:text-white transition-colors">Optical Character Recognition</a></li>
              <li><a href="#categories" className="hover:text-white transition-colors">6 Supported Categories</a></li>
              <li><a href="#how-it-works" className="hover:text-white transition-colors">Classification Pipeline</a></li>
              <li><a href="#architecture" className="hover:text-white transition-colors">TF-IDF & Logistic Regression</a></li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200 mb-4">Classification Targets</h4>
            <ul className="space-y-1.5 text-xs text-slate-400">
              <li>• Blood Test (CBC, Hematology)</li>
              <li>• Diabetes (HbA1c, Glucose)</li>
              <li>• Cardiology (ECG, Echo, Troponin)</li>
              <li>• Radiology (X-Ray, CT, MRI, USG)</li>
              <li>• Kidney (RFT, Creatinine, eGFR)</li>
              <li>• Liver (LFT, Bilirubin, Enzymes)</li>
            </ul>
          </div>

          {/* Medical Disclaimer */}
          <div>
            <div className="p-4 rounded-xl bg-slate-800/80 border border-slate-700/80">
              <div className="flex items-center gap-2 text-amber-400 mb-2">
                <ShieldAlert className="w-4 h-4 shrink-0" />
                <span className="text-xs font-bold uppercase tracking-wider">Clinical Disclaimer</span>
              </div>
              <p className="text-[11px] text-slate-300 leading-relaxed">
                MediScan AI is an automated document classification platform for archival and administrative sorting. It does <strong>not</strong> provide diagnostic interpretations, medical diagnoses, or treatment recommendations.
              </p>
            </div>
          </div>
        </div>

        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© {new Date().getFullYear()} MediScan AI. Built for Academic & Engineering Demonstration.</p>
          <div className="flex items-center gap-6">
            <span>Python Flask</span>
            <span>React & Vite</span>
            <span>Scikit-Learn NLP</span>
            <span>PyMuPDF & OCR</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default PublicFooter;
