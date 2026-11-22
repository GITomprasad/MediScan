import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import api from '../services/api';
import {
  FileText,
  Droplet,
  Layers,
  HeartPulse,
  Activity,
  UploadCloud,
  CheckCircle2,
  Clock,
  ArrowUpRight,
  TrendingUp,
  ShieldCheck,
  AlertCircle,
  Eye,
  Loader2,
  Sparkles
} from 'lucide-react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend
} from 'recharts';

const Dashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [recentReports, setRecentReports] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [monthlyData, setMonthlyData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError('');

      const [statsRes, recentRes, catRes, monthRes] = await Promise.all([
        api.get('/dashboard/stats'),
        api.get('/dashboard/recent'),
        api.get('/analytics/categories'),
        api.get('/analytics/monthly'),
      ]);

      if (statsRes.data?.success) setStats(statsRes.data.stats);
      if (recentRes.data?.success) setRecentReports(recentRes.data.reports || []);
      if (catRes.data?.success) setCategoryData(catRes.data.distribution || []);
      if (monthRes.data?.success) setMonthlyData(monthRes.data.monthly || []);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      setError('Could not load dashboard statistics. Please ensure the backend server is running.');
    } finally {
      setLoading(false);
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

  if (loading) {
    return (
      <div className="py-20 flex flex-col items-center justify-center gap-3">
        <Loader2 className="w-9 h-9 text-sky-600 animate-spin" />
        <p className="text-sm font-medium text-slate-600">Gathering clinical records & analytics...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden p-6 sm:p-8 rounded-2xl bg-gradient-to-r from-sky-700 via-blue-700 to-indigo-800 text-white shadow-lg shadow-sky-900/10">
        <div className="relative z-10 max-w-2xl space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/15 backdrop-blur-md text-xs font-semibold text-sky-100 mb-1">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI-Driven Healthcare Document Intelligence</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Medical Document Operations
          </h2>
          <p className="text-xs sm:text-sm text-sky-100 leading-relaxed font-normal">
            Upload clinical reports in PDF or image formats to automatically extract text and categorize documents across 6 specialized domains.
          </p>
          <div className="pt-2 flex items-center gap-3">
            <NavLink
              to="/upload"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white text-slate-900 font-semibold text-xs sm:text-sm shadow-md hover:bg-slate-50 transition-all active:scale-[0.98]"
            >
              <UploadCloud className="w-4 h-4 text-sky-600" />
              <span>Classify New Document</span>
            </NavLink>
            <NavLink
              to="/history"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-sky-900/40 hover:bg-sky-900/60 border border-white/20 text-white font-semibold text-xs sm:text-sm transition-all"
            >
              <span>View History</span>
            </NavLink>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 flex items-start gap-3 text-rose-700 text-xs">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {/* Real Statistics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Total Reports */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-xs flex flex-col justify-between hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Reports</span>
            <div className="w-9 h-9 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center">
              <FileText className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-3xl font-extrabold text-slate-900">{stats?.total_reports ?? 0}</span>
            <p className="text-[11px] text-slate-400 mt-1 flex items-center gap-1 font-medium">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" /> Fully Indexed
            </p>
          </div>
        </div>

        {/* Blood Test Reports */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-xs flex flex-col justify-between hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Blood Tests</span>
            <div className="w-9 h-9 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center">
              <Droplet className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-3xl font-extrabold text-slate-900">{stats?.blood_test_count ?? 0}</span>
            <p className="text-[11px] text-slate-400 mt-1 font-medium">Hematology & CBC</p>
          </div>
        </div>

        {/* Radiology Reports */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-xs flex flex-col justify-between hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Radiology</span>
            <div className="w-9 h-9 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
              <Layers className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-3xl font-extrabold text-slate-900">{stats?.radiology_count ?? 0}</span>
            <p className="text-[11px] text-slate-400 mt-1 font-medium">X-Ray, CT, MRI, USG</p>
          </div>
        </div>

        {/* Cardiology Reports */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-xs flex flex-col justify-between hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Cardiology</span>
            <div className="w-9 h-9 rounded-xl bg-pink-50 text-pink-600 flex items-center justify-center">
              <HeartPulse className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-3xl font-extrabold text-slate-900">{stats?.cardiology_count ?? 0}</span>
            <p className="text-[11px] text-slate-400 mt-1 font-medium">ECG, Echo & Enzymes</p>
          </div>
        </div>

        {/* Other Categories */}
        <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-xs flex flex-col justify-between hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Other Specialties</span>
            <div className="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <Activity className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <span className="text-3xl font-extrabold text-slate-900">{stats?.other_count ?? 0}</span>
            <p className="text-[11px] text-slate-400 mt-1 font-medium">Diabetes, Kidney, Liver</p>
          </div>
        </div>
      </div>

      {/* Analytics Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Category Distribution Pie / Ring Chart */}
        <div className="lg:col-span-5 p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Category Distribution</h3>
              <p className="text-xs text-slate-400">Classified documents across specialties</p>
            </div>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-slate-100 text-slate-600">
              Real Data
            </span>
          </div>

          <div className="flex-1 min-h-[260px] flex items-center justify-center">
            {categoryData.some((c) => c.count > 0) ? (
              <ResponsiveContainer width="100%" height={260}>
                <PieChart>
                  <Pie
                    data={categoryData.filter((c) => c.count > 0)}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={95}
                    paddingAngle={4}
                    dataKey="count"
                    nameKey="category"
                  >
                    {categoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(val, name) => [`${val} reports`, name]}
                    contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', fontSize: '12px' }}
                  />
                  <Legend
                    verticalAlign="bottom"
                    iconType="circle"
                    formatter={(value) => <span className="text-xs text-slate-600 font-medium">{value}</span>}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-center py-8">
                <FileText className="w-10 h-10 text-slate-300 mx-auto mb-2" />
                <p className="text-xs text-slate-500 font-medium">No documents uploaded yet.</p>
                <p className="text-[11px] text-slate-400">Upload reports to see specialty breakdown.</p>
              </div>
            )}
          </div>
        </div>

        {/* Monthly Activity Area Chart */}
        <div className="lg:col-span-7 p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Upload Activity Trends</h3>
              <p className="text-xs text-slate-400">Monthly document volume ingested into MediScan</p>
            </div>
            <div className="flex items-center gap-1.5 text-xs font-medium text-emerald-600">
              <TrendingUp className="w-4 h-4" />
              <span>Real-Time Logs</span>
            </div>
          </div>

          <div className="flex-1 min-h-[260px]">
            <ResponsiveContainer width="100%" height={260}>
              <AreaChart data={monthlyData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="uploadGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0284c7" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#0284c7" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
                <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
                <Tooltip
                  formatter={(value) => [`${value} uploads`, 'Volume']}
                  contentStyle={{ borderRadius: '12px', border: '1px solid #e2e8f0', fontSize: '12px' }}
                />
                <Area
                  type="monotone"
                  dataKey="uploads"
                  stroke="#0284c7"
                  strokeWidth={2.5}
                  fillOpacity={1}
                  fill="url(#uploadGradient)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Uploads Table */}
      <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h3 className="text-base font-bold text-slate-900">Recent Classifications</h3>
            <p className="text-xs text-slate-400">Latest medical records evaluated by the ML model</p>
          </div>
          <NavLink
            to="/history"
            className="inline-flex items-center gap-1 text-xs font-bold text-sky-600 hover:text-sky-700"
          >
            <span>View All Reports</span>
            <ArrowUpRight className="w-4 h-4" />
          </NavLink>
        </div>

        {recentReports.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b border-slate-100 text-slate-400 font-semibold uppercase tracking-wider">
                <tr>
                  <th className="pb-3 pl-2">Report / File</th>
                  <th className="pb-3">Specialty Category</th>
                  <th className="pb-3">Confidence</th>
                  <th className="pb-3">Date Uploaded</th>
                  <th className="pb-3">Status</th>
                  <th className="pb-3 text-right pr-2">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {recentReports.map((report) => (
                  <tr key={report.id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="py-3.5 pl-2 font-medium text-slate-800 flex items-center gap-2">
                      <FileText className="w-4 h-4 text-sky-600 shrink-0" />
                      <span className="truncate max-w-[200px]" title={report.filename}>
                        {report.filename}
                      </span>
                    </td>
                    <td className="py-3.5">
                      <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-semibold border ${getCategoryBadgeClass(report.predicted_category)}`}>
                        {report.predicted_category}
                      </span>
                    </td>
                    <td className="py-3.5 font-semibold text-slate-700">
                      <div className="flex items-center gap-2">
                        <div className="w-16 bg-slate-100 h-1.5 rounded-full overflow-hidden">
                          <div
                            className="bg-emerald-500 h-full rounded-full"
                            style={{ width: `${Math.round(report.confidence_score * 100)}%` }}
                          />
                        </div>
                        <span>{(report.confidence_score * 100).toFixed(1)}%</span>
                      </div>
                    </td>
                    <td className="py-3.5 text-slate-500">
                      {report.uploaded_at ? new Date(report.uploaded_at).toLocaleDateString() : 'N/A'}
                    </td>
                    <td className="py-3.5">
                      <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                        Completed
                      </span>
                    </td>
                    <td className="py-3.5 text-right pr-2">
                      <button
                        onClick={() => navigate(`/results/${report.id}`)}
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold text-sky-700 bg-sky-50 hover:bg-sky-100 transition-colors"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>Inspect</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="py-12 text-center rounded-xl bg-slate-50 border border-dashed border-slate-200">
            <UploadCloud className="w-10 h-10 text-slate-300 mx-auto mb-2" />
            <h4 className="text-sm font-semibold text-slate-700">No medical reports uploaded yet</h4>
            <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
              Get started by uploading your first medical report in PDF or image format to test the classification model.
            </p>
            <NavLink
              to="/upload"
              className="mt-4 inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-sky-600 text-white text-xs font-semibold hover:bg-sky-700 transition-colors"
            >
              <UploadCloud className="w-4 h-4" />
              <span>Upload Report Now</span>
            </NavLink>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
