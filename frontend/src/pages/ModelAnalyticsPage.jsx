import React, { useState, useEffect } from 'react';
import api from '../services/api';
import {
  BrainCircuit,
  CheckCircle2,
  BarChart3,
  Layers,
  Cpu,
  ShieldCheck,
  AlertCircle,
  Loader2,
  Sparkles,
  GitCommit
} from 'lucide-react';

const ModelAnalyticsPage = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      setLoading(true);
      setError('');
      const res = await api.get('/analytics/model-metrics');
      if (res.data?.success && res.data?.metrics) {
        setMetrics(res.data.metrics);
      }
    } catch (err) {
      console.error('Failed to load metrics:', err);
      setError('Could not load ML evaluation metrics.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="py-20 flex flex-col items-center justify-center gap-3">
        <Loader2 className="w-8 h-8 text-sky-600 animate-spin" />
        <p className="text-xs font-medium text-slate-500">Loading model evaluation metrics...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">ML Model Performance & Evaluation</h2>
        <p className="text-xs sm:text-sm text-slate-500">
          Empirical evaluation results computed on the held-out test dataset (25% stratified test split).
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}

      {metrics && (
        <>
          {/* Key Metric Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-xs">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Test Accuracy</span>
              <p className="text-3xl font-black text-sky-600 mt-2">
                {(metrics.accuracy * 100).toFixed(1)}%
              </p>
              <p className="text-[11px] text-slate-400 mt-1">Evaluated on {metrics.test_samples} unseen reports</p>
            </div>

            <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-xs">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Macro Precision</span>
              <p className="text-3xl font-black text-emerald-600 mt-2">
                {(metrics.precision_macro * 100).toFixed(1)}%
              </p>
              <p className="text-[11px] text-slate-400 mt-1">Balanced across all 6 classes</p>
            </div>

            <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-xs">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Macro Recall</span>
              <p className="text-3xl font-black text-blue-600 mt-2">
                {(metrics.recall_macro * 100).toFixed(1)}%
              </p>
              <p className="text-[11px] text-slate-400 mt-1">High sensitivity per specialty</p>
            </div>

            <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-xs">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Macro F1-Score</span>
              <p className="text-3xl font-black text-indigo-600 mt-2">
                {(metrics.f1_macro * 100).toFixed(1)}%
              </p>
              <p className="text-[11px] text-slate-400 mt-1">Harmonic mean of precision & recall</p>
            </div>
          </div>

          {/* Model Specification & Architecture */}
          <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs space-y-4">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center">
                <Cpu className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-900">Machine Learning Pipeline Specs</h3>
                <p className="text-xs text-slate-400">Model hyperparameters and training configuration</p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 text-xs">
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-slate-400 block font-medium">Algorithm</span>
                <span className="font-bold text-slate-800 text-sm block mt-0.5">Multinomial Logistic Regression</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-slate-400 block font-medium">Feature Extraction</span>
                <span className="font-bold text-slate-800 text-sm block mt-0.5">TF-IDF (1-gram & 2-gram)</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-slate-400 block font-medium">Dataset Size</span>
                <span className="font-bold text-slate-800 text-sm block mt-0.5">{metrics.total_samples} Clinical Reports</span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <span className="text-slate-400 block font-medium">Split Strategy</span>
                <span className="font-bold text-slate-800 text-sm block mt-0.5">Stratified (75% Train / 25% Test)</span>
              </div>
            </div>
          </div>

          {/* Confusion Matrix Heatmap */}
          {metrics.confusion_matrix && metrics.classes && (
            <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs space-y-4">
              <div>
                <h3 className="text-sm font-bold text-slate-900">Empirical Confusion Matrix</h3>
                <p className="text-xs text-slate-400">
                  Rows represent ground truth classes; columns represent model predictions.
                </p>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-center text-xs">
                  <thead>
                    <tr>
                      <th className="p-2 text-left text-slate-400 font-semibold">True \ Pred</th>
                      {metrics.classes.map((c, i) => (
                        <th key={i} className="p-2 font-semibold text-slate-700 whitespace-nowrap">
                          {c}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {metrics.confusion_matrix.map((row, rIdx) => (
                      <tr key={rIdx}>
                        <td className="p-2.5 text-left font-semibold text-slate-800 whitespace-nowrap">
                          {metrics.classes[rIdx]}
                        </td>
                        {row.map((val, cIdx) => {
                          const isDiagonal = rIdx === cIdx;
                          return (
                            <td
                              key={cIdx}
                              className={`p-2.5 font-bold rounded-lg transition-colors ${
                                isDiagonal && val > 0
                                  ? 'bg-emerald-100 text-emerald-800 font-extrabold'
                                  : val > 0
                                  ? 'bg-amber-100 text-amber-800'
                                  : 'text-slate-300'
                              }`}
                            >
                              {val}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Detailed Classification Report Table */}
          {metrics.classification_report && (
            <div className="p-6 rounded-2xl bg-white border border-slate-200/90 shadow-xs space-y-4">
              <div>
                <h3 className="text-sm font-bold text-slate-900">Per-Class Classification Metrics</h3>
                <p className="text-xs text-slate-400">Detailed precision, recall, and F1-score breakdown</p>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 border-b border-slate-100 text-slate-400 font-semibold uppercase tracking-wider">
                    <tr>
                      <th className="py-3 pl-4">Specialty Class</th>
                      <th className="py-3 px-3">Precision</th>
                      <th className="py-3 px-3">Recall</th>
                      <th className="py-3 px-3">F1-Score</th>
                      <th className="py-3 pr-4 text-right">Support</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {metrics.classes.map((clsName) => {
                      const item = metrics.classification_report[clsName];
                      if (!item) return null;
                      return (
                        <tr key={clsName} className="hover:bg-slate-50/70">
                          <td className="py-3 pl-4 font-bold text-slate-800">{clsName}</td>
                          <td className="py-3 px-3 text-slate-700">{(item.precision * 100).toFixed(1)}%</td>
                          <td className="py-3 px-3 text-slate-700">{(item.recall * 100).toFixed(1)}%</td>
                          <td className="py-3 px-3 font-semibold text-sky-700">{(item['f1-score'] * 100).toFixed(1)}%</td>
                          <td className="py-3 pr-4 text-right text-slate-500 font-mono">{item.support}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default ModelAnalyticsPage;
