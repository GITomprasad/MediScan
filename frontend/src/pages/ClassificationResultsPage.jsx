import React, { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate, NavLink } from 'react-router-dom';
import api from '../services/api';
import {
  FileText,
  Download,
  UploadCloud,
  CheckCircle2,
  Copy,
  Check,
  AlertTriangle,
  ArrowLeft,
  Droplet,
  Layers,
  HeartPulse,
  Activity,
  Syringe,
  Sparkles,
  ShieldAlert,
  Loader2,
  Calendar,
  FileCheck
} from 'lucide-react';

const ClassificationResultsPage = () => {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const [report, setReport] = useState(location.state?.report || null);
  const [loading, setLoading] = useState(!location.state?.report);
  const [downloading, setDownloading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!report && id) {
      fetchReport(id);
    }
  }, [id]);

  const fetchReport = async (reportId) => {
    try {
      setLoading(true);
      setError('');
      const res = await api.get(`/reports/${reportId}`);
      if (res.data?.success && res.data?.report) {
        setReport(res.data.report);
      } else {
        throw new Error(res.data?.message || 'Report not found');
      }
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Failed to load classification results.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!report?.id) return;
    try {
      setDownloading(true);
      const res = await api.get(`/reports/${report.id}/download`, {
        responseType: 'blob',
      });
      const blob = new Blob([res.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `MediScan_Report_${report.id}_${(report.predicted_category || '').replace(' ', '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download error:', err);
      alert('Failed to download PDF summary report.');
    } finally {
      setDownloading(false);
    }
  };

  const copyExtractedText = () => {
    if (!report?.extracted_text) return;
    navigator.clipboard.writeText(report.extracted_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getCategoryDetails = (cat) => {
    switch (cat) {
      case 'Blood Test':
        return {
          icon: Droplet,
          color: 'text-rose-600',
          bg: 'bg-rose-50 border-rose-200',
          pill: 'bg-rose-100 text-rose-800',
          desc: 'Hematology, Complete Blood Count (CBC), Red/White blood cells, Platelets, and Coagulation.'
        };
      case 'Diabetes':
        return {
          icon: Syringe,
          color: 'text-amber-600',
          bg: 'bg-amber-50 border-amber-200',
          pill: 'bg-amber-100 text-amber-800',
          desc: 'Endocrinology, Fasting / Postprandial Glucose, Glycated Hemoglobin (HbA1c), and Insulin.'
        };
      case 'Cardiology':
        return {
          icon: HeartPulse,
          color: 'text-pink-600',
          bg: 'bg-pink-50 border-pink-200',
          pill: 'bg-pink-100 text-pink-800',
          desc: 'Cardiovascular diagnostics, 12-Lead Electrocardiogram, 2D Echo LVEF, and Cardiac Troponins.'
        };
      case 'Radiology':
        return {
          icon: Layers,
          color: 'text-purple-600',
          bg: 'bg-purple-50 border-purple-200',
          pill: 'bg-purple-100 text-purple-800',
          desc: 'Diagnostic imaging, Chest Radiographs (X-Ray), Computed Tomography (CT), and Ultrasound.'
        };
      case 'Kidney':
        return {
          icon: Activity,
          color: 'text-cyan-600',
          bg: 'bg-cyan-50 border-cyan-200',
          pill: 'bg-cyan-100 text-cyan-800',
          desc: 'Nephrology, Renal Function Test (RFT/KFT), Serum Creatinine, Blood Urea Nitrogen (BUN), eGFR.'
        };
      case 'Liver':
        return {
          icon: Sparkles,
          color: 'text-emerald-600',
          bg: 'bg-emerald-50 border-emerald-200',
          pill: 'bg-emerald-100 text-emerald-800',
          desc: 'Hepatology, Liver Function Test (LFT), Bilirubin, Transaminases (SGPT/ALT, SGOT/AST), and ALP.'
        };
      default:
        return {
          icon: FileText,
          color: 'text-sky-600',
          bg: 'bg-sky-50 border-sky-200',
          pill: 'bg-sky-100 text-sky-800',
          desc: 'Clinical document evaluated by MediScan AI classifier.'
        };
    }
  };

  if (loading) {
    return (
      <div className="py-20 flex flex-col items-center justify-center gap-3">
        <Loader2 className="w-9 h-9 text-sky-600 animate-spin" />
        <p className="text-sm font-medium text-slate-600">Retrieving classification report...</p>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="max-w-xl mx-auto py-12 text-center space-y-4">
        <div className="w-12 h-12 rounded-2xl bg-rose-100 text-rose-600 flex items-center justify-center mx-auto">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <h3 className="text-lg font-bold text-slate-900">Report Unavailable</h3>
        <p className="text-xs text-slate-500">{error || 'Could not find the requested classification result.'}</p>
        <button
          onClick={() => navigate('/history')}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-semibold"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Report History</span>
        </button>
      </div>
    );
  }

  const categoryDetails = getCategoryDetails(report.predicted_category);
  const CategoryIcon = categoryDetails.icon;
  const confidencePct = Math.round((report.confidence_score || 0) * 100);

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Top Navigation & Status */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-800 transition-colors w-fit"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Reports</span>
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={handleDownloadPDF}
            disabled={downloading}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white border border-slate-200 text-slate-800 text-xs font-semibold hover:bg-slate-50 shadow-xs transition-all active:scale-[0.98]"
          >
            {downloading ? (
              <Loader2 className="w-4 h-4 text-sky-600 animate-spin" />
            ) : (
              <Download className="w-4 h-4 text-sky-600" />
            )}
            <span>Download Result as PDF</span>
          </button>

          <NavLink
            to="/upload"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-sky-600 text-white text-xs font-semibold hover:bg-sky-700 shadow-xs transition-all active:scale-[0.98]"
          >
            <UploadCloud className="w-4 h-4" />
            <span>Upload Another</span>
          </NavLink>
        </div>
      </div>

      {/* Main Classification Result Card */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
        {/* Header strip */}
        <div className="p-6 sm:p-8 border-b border-slate-100 flex flex-col md:flex-row md:items-center justify-between gap-6 bg-radial from-sky-50/50 via-white to-white">
          <div className="flex items-start gap-4">
            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center border ${categoryDetails.bg} ${categoryDetails.color} shadow-sm shrink-0`}>
              <CategoryIcon className="w-8 h-8 stroke-[2.2]" />
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                  Predicted Specialty
                </span>
                <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${categoryDetails.pill}`}>
                  Verified Match
                </span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                {report.predicted_category}
              </h2>
              <p className="text-xs text-slate-500 max-w-lg">
                {categoryDetails.desc}
              </p>
            </div>
          </div>

          {/* Model Confidence Meter */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 shrink-0 min-w-[190px]">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                Confidence
              </span>
              <span className="text-xs font-extrabold text-emerald-700 bg-emerald-100/80 px-2 py-0.5 rounded-md">
                {(report.confidence_score * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-slate-200 h-2.5 rounded-full overflow-hidden">
              <div
                className="bg-gradient-to-r from-emerald-500 to-teal-500 h-full rounded-full transition-all duration-700"
                style={{ width: `${confidencePct}%` }}
              />
            </div>
            <p className="text-[10px] text-slate-400 mt-2 flex items-center gap-1 font-medium">
              <CheckCircle2 className="w-3 h-3 text-emerald-500" /> Calibrated Scikit-Learn Model
            </p>
          </div>
        </div>

        {/* Metadata Details Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 divide-x divide-y sm:divide-y-0 divide-slate-100 border-b border-slate-100 text-xs">
          <div className="p-4">
            <span className="text-slate-400 block font-medium">File Name</span>
            <span className="font-semibold text-slate-800 truncate block mt-0.5" title={report.filename}>
              {report.filename}
            </span>
          </div>
          <div className="p-4">
            <span className="text-slate-400 block font-medium">Classification Date</span>
            <span className="font-semibold text-slate-800 block mt-0.5">
              {report.uploaded_at ? new Date(report.uploaded_at).toLocaleDateString() : 'N/A'}
            </span>
          </div>
          <div className="p-4">
            <span className="text-slate-400 block font-medium">Processing Status</span>
            <span className="inline-flex items-center gap-1 font-semibold text-emerald-700 mt-0.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              {report.processing_status ? report.processing_status.toUpperCase() : 'COMPLETED'}
            </span>
          </div>
          <div className="p-4">
            <span className="text-slate-400 block font-medium">Report Reference ID</span>
            <span className="font-mono font-semibold text-slate-800 block mt-0.5">
              #RPT-{report.id.toString().padStart(5, '0')}
            </span>
          </div>
        </div>

        {/* Extracted Clinical Text Preview Section */}
        <div className="p-6 sm:p-8 space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <FileCheck className="w-4 h-4 text-sky-600" />
                <span>Extracted Document Content</span>
              </h3>
              <p className="text-xs text-slate-400">
                Text recognized through OCR and digital extraction pipeline
              </p>
            </div>
            <button
              onClick={copyExtractedText}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-600" />
                  <span className="text-emerald-700">Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5 text-slate-400" />
                  <span>Copy Text</span>
                </>
              )}
            </button>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 font-mono text-xs text-slate-700 whitespace-pre-wrap leading-relaxed max-h-72 overflow-y-auto">
            {report.extracted_text || 'No text extracted.'}
          </div>
        </div>
      </div>

      {/* Prominent Clinical Disclaimer Callout */}
      <div className="p-5 rounded-2xl bg-amber-50/70 border border-amber-200 flex items-start gap-3.5">
        <ShieldAlert className="w-6 h-6 text-amber-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <h4 className="text-xs font-bold uppercase tracking-wider text-amber-900">
            Important Medical Disclaimer
          </h4>
          <p className="text-xs text-amber-800 leading-relaxed">
            MediScan AI is an automated document classification and document management system. 
            <strong> This tool does NOT provide medical diagnosis, treatment recommendations, or clinical advice. </strong>
            Classification outputs indicate document category and specialty indexing only. Always seek the advice of a qualified physician or healthcare provider regarding any medical condition or diagnostic result.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ClassificationResultsPage;
