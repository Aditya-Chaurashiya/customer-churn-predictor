import React, { useState } from 'react';
import { predictChurn } from '../services/api';
import RiskBadge from './RiskBadge';
import { PredictionResult } from '../types';

export default function PredictionForm() {
  const [formData, setFormData] = useState({
    tenure: 12,
    monthly_charges: 50,
    total_charges: 600,
    contract: 'Month-to-month',
    internet_service: 'Fiber optic',
    payment_method: 'Electronic check',
  });
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await predictChurn(formData);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <h3 className="text-lg font-medium mb-4">Customer Details</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Tenure (months)</label>
            <input type="number" value={formData.tenure} onChange={e => setFormData({...formData, tenure: Number(e.target.value)})} className="mt-1 block w-full rounded-md border-gray-300 border p-2 shadow-sm" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Monthly Charges</label>
            <input type="number" value={formData.monthly_charges} onChange={e => setFormData({...formData, monthly_charges: Number(e.target.value)})} className="mt-1 block w-full rounded-md border-gray-300 border p-2 shadow-sm" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Contract Type</label>
            <select value={formData.contract} onChange={e => setFormData({...formData, contract: e.target.value})} className="mt-1 block w-full rounded-md border-gray-300 border p-2 shadow-sm">
              <option>Month-to-month</option>
              <option>One year</option>
              <option>Two year</option>
            </select>
          </div>
          <button type="submit" disabled={loading} className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none">
            {loading ? 'Predicting...' : 'Run Prediction'}
          </button>
        </form>
      </div>

      {result && (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium mb-4">Prediction Result</h3>
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <span className="text-gray-500">Risk Level</span>
              <RiskBadge level={result.risk_level} />
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">Churn Probability</span>
                <span className="text-sm font-medium">{(result.churn_probability * 100).toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-red-500 h-2 rounded-full" style={{ width: `${result.churn_probability * 100}%` }}></div>
              </div>
            </div>
            
            <div>
              <h4 className="text-sm font-medium text-gray-900 mb-2">Risk Factors</h4>
              <ul className="list-disc pl-5 text-sm text-red-600 space-y-1">
                {result.risk_factors.map((f, i) => <li key={i}>{f}</li>)}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
