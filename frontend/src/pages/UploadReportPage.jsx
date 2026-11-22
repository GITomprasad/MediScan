import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import {
  UploadCloud,
  FileText,
  Image as ImageIcon,
  X,
  AlertCircle,
  CheckCircle2,
  Loader2,
  FileCheck2,
  Cpu,
  ScanText,
  ShieldCheck,
  Sparkles
} from 'lucide-react';

const ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg'];
const MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024; // 10MB

const UploadReportPage = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [filePreview, setFilePreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progressStage, setProgressStage] = useState(0);
  const [errorMessage, setErrorMessage] = useState('');

  const stageMessages = [
    { title: 'Uploading Document', desc: 'Securely transferring medical file to ingestion server...', icon: UploadCloud },
    { title: 'OCR & Digital Text Extraction', desc: 'PyMuPDF and Optical Character Recognition parsing document content...', icon: ScanText },
    { title: 'NLP TF-IDF Feature Engineering', desc: 'Tokenizing clinical biomarkers, medical bigrams, and lab terms...', icon: Cpu },
    { title: 'Machine Learning Classification', desc: 'Calibrated classifier evaluating specialty probabilities...', icon: Sparkles }
  ];

  const handleFile = (file) => {
    setErrorMessage('');
    if (!file) return;

    const ext = file.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(ext)) {
      setErrorMessage(`Unsupported format .${ext}. Only PDF, PNG, JPG, and JPEG documents are permitted.`);
      return;
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      setErrorMessage(`File size (${(file.size / (1024 * 1024)).toFixed(2)} MB) exceeds the 10 MB limit.`);
      return;
    }

    if (file.size === 0) {
      setErrorMessage('The selected file is empty (0 bytes).');
      return;
    }

    setSelectedFile(file);

    // Generate preview for images
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => setFilePreview(e.target.result);
      reader.readAsDataURL(file);
    } else {
      setFilePreview(null);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    setFilePreview(null);
    setErrorMessage('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setErrorMessage('Please select a medical report file to classify.');
      return;
    }

    try {
      setUploading(true);
      setErrorMessage('');
      setProgressStage(0);

      // Multi-stage progress animation
      const stageTimer1 = setTimeout(() => setProgressStage(1), 500);
      const stageTimer2 = setTimeout(() => setProgressStage(2), 1100);
      const stageTimer3 = setTimeout(() => setProgressStage(3), 1700);

      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await api.post('/reports/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      clearTimeout(stageTimer1);
      clearTimeout(stageTimer2);
      clearTimeout(stageTimer3);

      if (response.data?.success && response.data?.report) {
        const reportId = response.data.report.id;
        navigate(`/results/${reportId}`, {
          state: {
            report: response.data.report,
            isNewUpload: true
          }
        });
      } else {
        throw new Error(response.data?.message || 'Failed to process document');
      }
    } catch (err) {
      console.error('Classification error:', err);
      const msg = err.response?.data?.message || err.message || 'An error occurred during OCR extraction or ML inference.';
      setErrorMessage(msg);
    } finally {
      setUploading(false);
      setProgressStage(0);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header Info */}
      <div className="text-left space-y-1">
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Upload Medical Document</h2>
        <p className="text-xs sm:text-sm text-slate-500">
          Upload any medical test, laboratory printout, or radiology scan. Our OCR & NLP pipeline will extract text and predict the category.
        </p>
      </div>

      {/* Error Banner */}
      {errorMessage && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 flex items-start gap-3 text-rose-700 text-xs">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5 text-rose-600" />
          <div className="space-y-1">
            <p className="font-semibold text-rose-800">Processing Error</p>
            <p>{errorMessage}</p>
          </div>
        </div>
      )}

      {/* Main Upload Card */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-6 sm:p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={handleFileInputChange}
            className="hidden"
          />

          {!selectedFile ? (
            /* Drag and Drop Box */
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-8 sm:p-12 text-center cursor-pointer transition-all ${
                dragActive
                  ? 'border-sky-500 bg-sky-50/60 scale-[1.01]'
                  : 'border-slate-300 hover:border-sky-400 bg-slate-50/50 hover:bg-slate-50'
              }`}
            >
              <div className="w-16 h-16 rounded-2xl bg-sky-100 text-sky-600 flex items-center justify-center mx-auto mb-4 shadow-xs">
                <UploadCloud className="w-8 h-8" />
              </div>

              <h3 className="text-base font-bold text-slate-800 mb-1">
                Drag and drop your medical report here
              </h3>
              <p className="text-xs text-slate-500 mb-4">
                or <span className="text-sky-600 font-semibold underline underline-offset-2">browse files</span> from your computer
              </p>

              <div className="flex flex-wrap items-center justify-center gap-2 max-w-sm mx-auto">
                <span className="px-2.5 py-1 rounded-md bg-white border border-slate-200 text-[11px] font-semibold text-slate-600">PDF</span>
                <span className="px-2.5 py-1 rounded-md bg-white border border-slate-200 text-[11px] font-semibold text-slate-600">PNG</span>
                <span className="px-2.5 py-1 rounded-md bg-white border border-slate-200 text-[11px] font-semibold text-slate-600">JPG</span>
                <span className="px-2.5 py-1 rounded-md bg-white border border-slate-200 text-[11px] font-semibold text-slate-600">JPEG</span>
                <span className="text-[11px] text-slate-400 font-medium">Max 10 MB</span>
              </div>
            </div>
          ) : (
            /* Selected File Preview */
            <div className="rounded-2xl border border-slate-200 bg-slate-50/70 p-5 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-12 h-12 rounded-xl bg-white border border-slate-200 text-sky-600 flex items-center justify-center shadow-xs shrink-0">
                    {selectedFile.type.startsWith('image/') ? (
                      <ImageIcon className="w-6 h-6 text-sky-600" />
                    ) : (
                      <FileText className="w-6 h-6 text-rose-500" />
                    )}
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-bold text-slate-800 truncate">{selectedFile.name}</p>
                    <p className="text-xs text-slate-400">
                      {(selectedFile.size / 1024).toFixed(1)} KB • {selectedFile.type || 'application/pdf'}
                    </p>
                  </div>
                </div>

                {!uploading && (
                  <button
                    type="button"
                    onClick={removeFile}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                    title="Remove selected file"
                  >
                    <X className="w-5 h-5" />
                  </button>
                )}
              </div>

              {/* Image Preview Thumbnail if available */}
              {filePreview && (
                <div className="mt-2 rounded-xl overflow-hidden border border-slate-200 max-h-56 flex items-center justify-center bg-slate-900/5 p-2">
                  <img
                    src={filePreview}
                    alt="Document preview"
                    className="max-h-52 object-contain rounded-lg"
                  />
                </div>
              )}
            </div>
          )}

          {/* Upload & Progress State */}
          {uploading && (
            <div className="p-6 rounded-2xl bg-sky-50/80 border border-sky-200/80 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Loader2 className="w-5 h-5 text-sky-600 animate-spin" />
                  <span className="text-xs font-bold text-sky-900 uppercase tracking-wider">
                    Analyzing Document
                  </span>
                </div>
                <span className="text-xs font-bold text-sky-700">
                  Stage {progressStage + 1} of 4
                </span>
              </div>

              {/* Progress bar */}
              <div className="w-full bg-sky-200 h-2 rounded-full overflow-hidden">
                <div
                  className="bg-sky-600 h-full rounded-full transition-all duration-500"
                  style={{ width: `${((progressStage + 1) / 4) * 100}%` }}
                />
              </div>

              <div className="flex items-start gap-3 pt-1">
                {React.createElement(stageMessages[progressStage].icon, {
                  className: 'w-5 h-5 text-sky-700 shrink-0 mt-0.5'
                })}
                <div>
                  <p className="text-xs font-bold text-sky-900">
                    {stageMessages[progressStage].title}
                  </p>
                  <p className="text-[11px] text-sky-700">
                    {stageMessages[progressStage].desc}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <ShieldCheck className="w-4 h-4 text-emerald-500 shrink-0" />
              <span>Extracted medical data is processed privately & securely.</span>
            </div>

            <button
              type="submit"
              disabled={!selectedFile || uploading}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3 rounded-xl bg-gradient-to-r from-sky-600 to-blue-600 text-white font-semibold text-sm shadow-md hover:from-sky-700 hover:to-blue-700 focus:outline-hidden focus:ring-2 focus:ring-sky-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-[0.99]"
            >
              {uploading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Classifying Document...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Process & Classify Report</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Helpful Hint Card */}
      <div className="p-5 rounded-2xl bg-white border border-slate-200/80 shadow-xs space-y-2">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
          <FileCheck2 className="w-4 h-4 text-sky-600" />
          <span>Recommended Medical Test Reports for Best Results:</span>
        </h4>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 text-xs text-slate-600">
          <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
            <strong>Blood Test:</strong> CBC, Platelets, Hemoglobin, Hematocrit, ESR
          </div>
          <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
            <strong>Diabetes:</strong> Fasting Blood Glucose, Postprandial, HbA1c, OGTT
          </div>
          <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
            <strong>Cardiology:</strong> ECG Report, 2D Echo LVEF, Troponin I, CK-MB
          </div>
          <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
            <strong>Radiology:</strong> Chest X-Ray PA, CT Scan Thorax/Brain, USG Abdomen
          </div>
          <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
            <strong>Kidney:</strong> Renal Function Test (RFT/KFT), Creatinine, BUN, eGFR
          </div>
          <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
            <strong>Liver:</strong> Liver Function Test (LFT), Bilirubin, SGPT/ALT, SGOT
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadReportPage;
