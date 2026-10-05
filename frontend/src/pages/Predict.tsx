import React, { useState } from 'react';
import { predictSingle, predictBatch } from '../services/api';

const Predict = () => {
  const [formData, setFormData] = useState({
    customer_id: 'TEST-1234',
    gender: 'Female',
    senior_citizen: 0,
    partner: 'Yes',
    dependents: 'No',
    tenure: 12,
    phone_service: 'Yes',
    multiple_lines: 'No',
    internet_service: 'Fiber optic',
    online_security: 'No',
    online_backup: 'Yes',
    device_protection: 'No',
    tech_support: 'No',
    streaming_tv: 'Yes',
    streaming_movies: 'No',
    contract: 'Month-to-month',
    paperless_billing: 'Yes',
    payment_method: 'Electronic check',
    monthly_charges: 85.5,
    total_charges: 1026.0
  });

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  
  const [file, setFile] = useState<File | null>(null);
  const [batchResult, setBatchResult] = useState<any[] | null>(null);
  const [batchLoading, setBatchLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: ['tenure', 'monthly_charges', 'total_charges', 'senior_citizen'].includes(name) 
        ? Number(value) 
        : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await predictSingle(formData);
      setResult(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleBatchUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setBatchLoading(true);
    const fd = new FormData();
    fd.append('file', file);
    try {
      const res = await predictBatch(fd);
      setBatchResult(res.data.results);
    } catch (e) {
      console.error(e);
    } finally {
      setBatchLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div className="bg-white p-6 rounded-lg shadow border">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">Individual Prediction</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-gray-500 mb-1">Customer ID</label>
              <input name="customer_id" value={formData.customer_id} onChange={handleChange} className="w-full border p-2 rounded text-sm" />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Tenure (months)</label>
              <input type="number" name="tenure" value={formData.tenure} onChange={handleChange} className="w-full border p-2 rounded text-sm" />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Contract</label>
              <select name="contract" value={formData.contract} onChange={handleChange} className="w-full border p-2 rounded text-sm bg-white">
                <option value="Month-to-month">Month-to-month</option>
                <option value="One year">One year</option>
                <option value="Two year">Two year</option>
              </select>
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Monthly Charges</label>
              <input type="number" step="0.01" name="monthly_charges" value={formData.monthly_charges} onChange={handleChange} className="w-full border p-2 rounded text-sm" />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Total Charges</label>
              <input type="number" step="0.01" name="total_charges" value={formData.total_charges} onChange={handleChange} className="w-full border p-2 rounded text-sm" />
            </div>
            <div>
              <label className="block text-xs text-gray-500 mb-1">Internet Service</label>
              <select name="internet_service" value={formData.internet_service} onChange={handleChange} className="w-full border p-2 rounded text-sm bg-white">
                <option value="DSL">DSL</option>
                <option value="Fiber optic">Fiber optic</option>
                <option value="No">No</option>
              </select>
            </div>
          </div>
          
          <button type="submit" disabled={loading} className="w-full bg-indigo-600 text-white p-2 rounded hover:bg-indigo-700 disabled:opacity-50">
            {loading ? 'Predicting...' : 'Predict Churn Risk'}
          </button>
        </form>

        {result && (
          <div className={`mt-6 p-4 rounded-lg border ${result.prediction === 'Likely to Churn' ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
            <h4 className="font-semibold text-gray-800 mb-2">Prediction Result</h4>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <span className="text-gray-500">Prediction:</span>
              <span className="font-medium">{result.prediction}</span>
              <span className="text-gray-500">Probability:</span>
              <span className="font-medium">{(result.churn_probability * 100).toFixed(1)}%</span>
              <span className="text-gray-500">Risk Level:</span>
              <span className="font-medium">{result.risk_level}</span>
            </div>
          </div>
        )}
      </div>

      <div className="bg-white p-6 rounded-lg shadow border">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">Batch Prediction</h3>
        <form onSubmit={handleBatchUpload} className="space-y-4">
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
            <input 
              type="file" 
              accept=".csv"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="mb-2"
            />
            <p className="text-sm text-gray-500">Upload a CSV file containing customer records</p>
          </div>
          <button type="submit" disabled={!file || batchLoading} className="w-full bg-gray-800 text-white p-2 rounded hover:bg-gray-900 disabled:opacity-50">
            {batchLoading ? 'Processing Batch...' : 'Run Batch Prediction'}
          </button>
        </form>
        
        {batchResult && (
          <div className="mt-6">
            <h4 className="font-semibold text-gray-800 mb-2">Batch Results ({batchResult.length} processed)</h4>
            <div className="max-h-64 overflow-y-auto border rounded">
              <table className="min-w-full divide-y divide-gray-200 text-sm">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-2 text-left">ID</th>
                    <th className="px-4 py-2 text-left">Prob</th>
                    <th className="px-4 py-2 text-left">Risk</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {batchResult.slice(0, 50).map((r, i) => (
                    <tr key={i}>
                      <td className="px-4 py-2">{r.customer_id}</td>
                      <td className="px-4 py-2">{(r.churn_probability * 100).toFixed(1)}%</td>
                      <td className="px-4 py-2">{r.risk_level}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {batchResult.length > 50 && <p className="text-xs text-gray-500 mt-2">Showing first 50 results</p>}
          </div>
        )}
      </div>
    </div>
  );
};

export default Predict;
