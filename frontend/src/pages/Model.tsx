import React, { useState, useEffect } from 'react';
import { fetchModelPerformance, fetchConfusionMatrix, fetchTopIndicators, retrainModel } from '../services/api';
import { ModelMetrics, ConfusionMatrix, ChurnIndicator } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from 'recharts';

export default function Model() {
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);
  const [matrix, setMatrix] = useState<ConfusionMatrix | null>(null);
  const [indicators, setIndicators] = useState<ChurnIndicator[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retraining, setRetraining] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [m, mat, ind] = await Promise.all([
        fetchModelPerformance(),
        fetchConfusionMatrix(),
        fetchTopIndicators()
      ]);
      setMetrics(m);
      setMatrix(mat);
      setIndicators(ind);
    } catch (e) {
      setError('Failed to fetch model info.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRetrain = async () => {
    setRetraining(true);
    try {
      await retrainModel();
      alert('Model retrained successfully');
      loadData();
    } catch (e) {
      alert('Retraining failed');
    } finally {
      setRetraining(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={loadData} />;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Model Performance</h1>
          <p className="text-gray-500 mt-1">Version: {metrics?.version}</p>
        </div>
        <button 
          onClick={handleRetrain}
          disabled={retraining}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {retraining ? 'Retraining...' : 'Retrain Model'}
        </button>
      </div>

      {metrics && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 text-center">
            <div className="text-sm text-gray-500">Accuracy</div>
            <div className="text-2xl font-bold text-green-600">{(metrics.accuracy * 100).toFixed(1)}%</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 text-center">
            <div className="text-sm text-gray-500">Precision</div>
            <div className="text-2xl font-bold text-blue-600">{(metrics.precision_score * 100).toFixed(1)}%</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 text-center">
            <div className="text-sm text-gray-500">Recall</div>
            <div className="text-2xl font-bold text-purple-600">{(metrics.recall * 100).toFixed(1)}%</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 text-center">
            <div className="text-sm text-gray-500">F1 Score</div>
            <div className="text-2xl font-bold text-orange-600">{(metrics.f1_score * 100).toFixed(1)}%</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 text-center">
            <div className="text-sm text-gray-500">ROC AUC</div>
            <div className="text-2xl font-bold text-indigo-600">{(metrics.roc_auc * 100).toFixed(1)}%</div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-96">
          <h3 className="text-lg font-medium mb-4">Top Churn Indicators</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart layout="vertical" data={indicators} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="feature" type="category" width={100} tick={{fontSize: 12}} />
              <RechartsTooltip />
              <Bar dataKey="importance" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {matrix && (
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-lg font-medium mb-4">Confusion Matrix</h3>
            <div className="grid grid-cols-3 gap-2 text-center h-full items-center">
              <div></div>
              <div className="font-semibold">Predicted Churn</div>
              <div className="font-semibold">Predicted Retained</div>
              
              <div className="font-semibold flex items-center justify-end pr-4">Actual Churn</div>
              <div className="bg-green-100 p-4 rounded text-green-800 flex flex-col">
                <span className="text-sm">True Positive</span>
                <span className="text-xl font-bold">{matrix.true_positive}</span>
              </div>
              <div className="bg-red-100 p-4 rounded text-red-800 flex flex-col">
                <span className="text-sm">False Negative</span>
                <span className="text-xl font-bold">{matrix.false_negative}</span>
              </div>
              
              <div className="font-semibold flex items-center justify-end pr-4">Actual Retained</div>
              <div className="bg-red-100 p-4 rounded text-red-800 flex flex-col">
                <span className="text-sm">False Positive</span>
                <span className="text-xl font-bold">{matrix.false_positive}</span>
              </div>
              <div className="bg-green-100 p-4 rounded text-green-800 flex flex-col">
                <span className="text-sm">True Negative</span>
                <span className="text-xl font-bold">{matrix.true_negative}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
