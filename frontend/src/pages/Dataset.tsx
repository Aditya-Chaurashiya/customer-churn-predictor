import React, { useState, useEffect } from 'react';
import { fetchDatasetInfo, uploadDataset } from '../services/api';
import { DatasetInfo } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

export default function Dataset() {
  const [info, setInfo] = useState<DatasetInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchDatasetInfo();
      setInfo(data);
    } catch (e) {
      setError('Failed to fetch dataset info.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      try {
        await uploadDataset(file);
        loadData();
      } catch (err) {
        alert('Upload failed');
      }
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={loadData} />;

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Dataset Management</h1>
        <p className="text-gray-500 mt-1">Manage training data and perform validations.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium mb-4">Current Dataset</h3>
          {info && (
            <div className="space-y-3 text-sm">
              <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Source</span><span className="font-medium">{info.source}</span></div>
              <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Total Records</span><span className="font-medium">{info.total_records.toLocaleString()}</span></div>
              <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Real Records</span><span className="font-medium">{info.real_records.toLocaleString()}</span></div>
              <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Synthetic Records</span><span className="font-medium">{info.synthetic_records.toLocaleString()}</span></div>
              <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Missing Values</span><span className="font-medium text-green-600">{info.missing_values || 0}</span></div>
            </div>
          )}
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium mb-4">Upload New Dataset</h3>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            <input type="file" accept=".csv" onChange={handleUpload} className="mb-4" />
            <p className="text-sm text-gray-500">Upload a clean CSV file to append or replace current training data.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
