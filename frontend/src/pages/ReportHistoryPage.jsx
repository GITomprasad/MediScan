import React, { useState, useEffect } from 'react';
import { useNavigate, NavLink } from 'react-router-dom';
import api from '../services/api';
import {
  FileText,
  Search,
  Filter,
  Download,
  Trash2,
  Eye,
  Calendar,
  CheckCircle2,
  AlertCircle,
  Loader2,
  UploadCloud,
  ChevronDown,
  ArrowUpDown,
  X
} from 'lucide-react';

const CATEGORIES = [
  'All',
  'Blood Test',
  'Diabetes',
  'Cardiology',
  'Radiology',
  'Kidney',
  'Liver'
];

const ReportHistoryPage = () => {
  const navigate = useNavigate();

  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [sortBy, setSortBy] = useState('newest');
  const [deleteModalReport, setDeleteModalReport] = useState(null);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchReports();
  }, [selectedCategory, sortBy]);

  const fetchReports = async () => {
    try {
      setLoading(true);
      setError('');

      let url = `/reports?sort=${sortBy}`;
      if (selectedCategory && selectedCategory !== 'All') {
        url += `&category=${encodeURIComponent(selectedCategory)}`;
      }
      if (searchTerm.trim()) {
        url += `&q=${encodeURIComponent(searchTerm.trim())}`;
      }

      const res = await api.get(url);
      if (res.data?.success) {
        setReports(res.data.reports || []);
      }
    } catch (err) {
      console.error('Fetch reports error:', err);
      setError('Failed to load reports. Please try refreshing.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchReports();
  };

  const handleDownloadPDF = async (reportId, filename, category) => {
    try {
      const res = await api.get(`/reports/${reportId}/download`, {
        responseType: 'blob',
      });
      const blob = new Blob([res.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `MediScan_Report_${reportId}_${category.replace(' ', '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download error:', err);
      alert('Failed to download report PDF.');
    }
  };

  const confirmDelete = async () => {
    if (!deleteModalReport) return;
    try {
      setDeleting(true);
      const res = await api.delete(`/reports/${deleteModalReport.id}`);
      if (res.data?.success) {
        setReports(reports.filter((r) => r.id !== deleteModalReport.id));
        setDeleteModalReport(null);
      }
    } catch (err) {
      alert(err.response?.data?.message || 'Failed to delete report.');
    } finally {
      setDeleting(false);
    }
  };

  const getCategoryBadgeClass = (category) => {
    switch (category) {
      case 'Blood Test':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      case 'Diabetes':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'Cardiology':
        return 'bg-pink-50 text-pink-700 border-pink-200';
      case 'Radiology':
        return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'Kidney':
        return 'bg-cyan-50 text-cyan-700 border-cyan-200';
      case 'Liver':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      default:
        return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Report History</h2>
          <p className="text-xs sm:text-sm text-slate-500">
            View, search, filter, download, and manage all previously analyzed medical reports.
          </p>
        </div>

        <NavLink
          to="/upload"
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-sky-600 text-white text-xs sm:text-sm font-semibold hover:bg-sky-700 shadow-xs transition-all active:scale-[0.98] w-fit"
        >
          <UploadCloud className="w-4 h-4" />
          <span>Upload New Report</span>
        </NavLink>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-xs space-y-3 sm:space-y-0 sm:flex sm:items-center sm:gap-4">
        {/* Search Input */}
        <form onSubmit={handleSearchSubmit} className="relative flex-1">
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <Search className="w-4 h-4" />
          </div>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by filename, category, or clinical text..."
            className="w-full pl-10 pr-4 py-2 rounded-xl border border-slate-200 text-xs sm:text-sm focus:outline-hidden focus:ring-2 focus:ring-sky-500 focus:border-transparent text-slate-800 placeholder-slate-400"
          />
        </form>

        {/* Category Dropdown */}
        <div className="flex items-center gap-2">
          <div className="relative min-w-[150px]">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full appearance-none pl-3 pr-8 py-2 rounded-xl border border-slate-200 bg-white text-xs sm:text-sm font-medium text-slate-700 focus:outline-hidden focus:ring-2 focus:ring-sky-500"
            >
              {CATEGORIES.map((cat) => (
                <option key={cat} value={cat}>
                  {cat === 'All' ? 'All Categories' : cat}
                </option>
              ))}
            </select>
            <ChevronDown className="w-4 h-4 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none" />
          </div>

          {/* Sort Dropdown */}
          <div className="relative min-w-[140px]">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="w-full appearance-none pl-3 pr-8 py-2 rounded-xl border border-slate-200 bg-white text-xs sm:text-sm font-medium text-slate-700 focus:outline-hidden focus:ring-2 focus:ring-sky-500"
            >
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="confidence_high">Highest Confidence</option>
              <option value="confidence_low">Lowest Confidence</option>
            </select>
            <ArrowUpDown className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-3 pointer-events-none" />
          </div>
        </div>
      </div>

      {/* Reports Table Card */}
      <div className="bg-white rounded-2xl border border-slate-200/90 shadow-xs overflow-hidden">
        {loading ? (
          <div className="py-20 flex flex-col items-center justify-center gap-3">
            <Loader2 className="w-8 h-8 text-sky-600 animate-spin" />
            <p className="text-xs font-medium text-slate-500">Querying database records...</p>
          </div>
        ) : reports.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-100 text-slate-400 font-semibold uppercase tracking-wider">
                <tr>
                  <th className="py-3.5 pl-6">Report File</th>
                  <th className="py-3.5 px-4">Specialty Category</th>
                  <th className="py-3.5 px-4">Confidence</th>
                  <th className="py-3.5 px-4">Upload Date</th>
                  <th className="py-3.5 px-4">Status</th>
                  <th className="py-3.5 pr-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {reports.map((report) => (
                  <tr key={report.id} className="hover:bg-slate-50/70 transition-colors">
                    {/* Filename */}
                    <td className="py-4 pl-6 font-semibold text-slate-800">
                      <div className="flex items-center gap-3 min-w-[200px]">
                        <div className="w-8 h-8 rounded-lg bg-sky-50 text-sky-600 flex items-center justify-center shrink-0">
                          <FileText className="w-4 h-4" />
                        </div>
                        <div className="min-w-0">
                          <span className="truncate block font-semibold text-slate-800 hover:text-sky-600 cursor-pointer" onClick={() => navigate(`/results/${report.id}`)} title={report.filename}>
                            {report.filename}
                          </span>
                          <span className="text-[10px] text-slate-400 font-mono">
                            #RPT-{report.id.toString().padStart(4, '0')}
                          </span>
                        </div>
                      </div>
                    </td>

                    {/* Category */}
                    <td className="py-4 px-4">
                      <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-semibold border ${getCategoryBadgeClass(report.predicted_category)}`}>
                        {report.predicted_category}
                      </span>
                    </td>

                    {/* Confidence */}
                    <td className="py-4 px-4 font-semibold text-slate-700">
                      <div className="flex items-center gap-2">
                        <div className="w-16 bg-slate-100 h-1.5 rounded-full overflow-hidden">
                          <div
                            className="bg-emerald-500 h-full rounded-full"
                            style={{ width: `${Math.round(report.confidence_score * 100)}%` }}
                          />
                        </div>
                        <span className="text-slate-800">
                          {(report.confidence_score * 100).toFixed(1)}%
                        </span>
                      </div>
                    </td>

                    {/* Date */}
                    <td className="py-4 px-4 text-slate-500 whitespace-nowrap">
                      {report.uploaded_at ? new Date(report.uploaded_at).toLocaleDateString() : 'N/A'}
                    </td>

                    {/* Status */}
                    <td className="py-4 px-4">
                      <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                        Completed
                      </span>
                    </td>

                    {/* Actions */}
                    <td className="py-4 pr-6 text-right whitespace-nowrap">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          onClick={() => navigate(`/results/${report.id}`)}
                          title="View Details"
                          className="p-1.5 rounded-lg text-slate-500 hover:text-sky-600 hover:bg-sky-50 transition-colors"
                        >
                          <Eye className="w-4 h-4" />
                        </button>

                        <button
                          onClick={() => handleDownloadPDF(report.id, report.filename, report.predicted_category)}
                          title="Download PDF Summary"
                          className="p-1.5 rounded-lg text-slate-500 hover:text-emerald-600 hover:bg-emerald-50 transition-colors"
                        >
                          <Download className="w-4 h-4" />
                        </button>

                        <button
                          onClick={() => setDeleteModalReport(report)}
                          title="Delete Report"
                          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="py-16 text-center space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
              <FileText className="w-6 h-6" />
            </div>
            <h4 className="text-sm font-semibold text-slate-700">No medical reports match your filter</h4>
            <p className="text-xs text-slate-400 max-w-sm mx-auto">
              Try adjusting your search keywords or category filters, or upload a new medical document.
            </p>
            <NavLink
              to="/upload"
              className="mt-2 inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-sky-600 text-white text-xs font-semibold hover:bg-sky-700 transition-colors"
            >
              <UploadCloud className="w-4 h-4" />
              <span>Upload Document</span>
            </NavLink>
          </div>
        )}
      </div>

      {/* Delete Confirmation Modal */}
      {deleteModalReport && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between">
              <div className="w-10 h-10 rounded-xl bg-rose-100 text-rose-600 flex items-center justify-center">
                <Trash2 className="w-5 h-5" />
              </div>
              <button
                onClick={() => setDeleteModalReport(null)}
                className="p-1 text-slate-400 hover:text-slate-600 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div>
              <h3 className="text-base font-bold text-slate-900">Delete Medical Report</h3>
              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                Are you sure you want to delete <strong className="text-slate-800">{deleteModalReport.filename}</strong>? This action cannot be undone and will remove the record and OCR extracted text from the database.
              </p>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setDeleteModalReport(null)}
                className="px-4 py-2 rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={confirmDelete}
                disabled={deleting}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-rose-600 text-white text-xs font-semibold hover:bg-rose-700 transition-colors disabled:opacity-60"
              >
                {deleting && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
                <span>Delete Report</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReportHistoryPage;
