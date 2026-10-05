import React, { useState } from 'react';
import PredictionForm from '../components/PredictionForm';
import { predictBatch } from '../services/api';

export default function Predictions() {
  const [activeTab, setActiveTab] = useState<'single' | 'batch'>('single');
  const [file, setFile] = useState<File | null>(null);
  const [batchResult, setBatchResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const res = await predictBatch(file);
      setBatchResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Predictions Simulator</h1>
        <p className="text-gray-500 mt-1">Run single predictions or process batch files.</p>
      </div>

      <div className="mb-6 border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('single')}
            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'single'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Single Prediction
          </button>
          <button
            onClick={() => setActiveTab('batch')}
            className={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'batch'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Batch Processing
          </button>
        </nav>
      </div>

      {activeTab === 'single' ? (
        <PredictionForm />
      ) : (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium mb-4">Batch Processing</h3>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center">
            <input 
              type="file" 
              accept=".csv" 
              onChange={e => setFile(e.target.files?.[0] || null)} 
              className="mb-4"
            />
            <p className="text-sm text-gray-500">Upload a CSV file containing customer data.</p>
            <button 
              onClick={handleFileUpload} 
              disabled={!file || loading}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Processing...' : 'Process Batch'}
            </button>
          </div>
          
          {batchResult && (
            <div className="mt-8">
              <h4 className="font-medium mb-2">Results Summary</h4>
              <p>Processed {batchResult.processed} records successfully.</p>
              {/* Display results table or download button here */}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
