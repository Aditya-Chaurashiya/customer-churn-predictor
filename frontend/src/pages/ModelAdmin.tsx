import React, { useEffect, useState } from 'react';
import axios from 'axios';
import api from '../services/api';
import { Target, Activity, Calendar } from 'lucide-react';

const ModelAdmin = () => {
  const [modelData, setModelData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [retraining, setRetraining] = useState(false);
  const [message, setMessage] = useState('');

  const fetchModel = async () => {
    try {
      const res = await api.get('/model/status');
      if (res.data.status) {
        setMessage(res.data.status);
      } else {
        setModelData(res.data);
      }
    } catch (e: any) {
      console.error(e);
      setMessage(e.message || "Failed to load model data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchModel();
  }, []);

  const handleRetrain = async () => {
    setRetraining(true);
    setMessage('');
    try {
      const res = await api.post('/model/retrain');
      setMessage(res.data.status || 'Retraining started. Check back later.');
    } catch (e: any) {
      console.error(e);
      setMessage('Failed to start retraining');
    } finally {
      setRetraining(false);
    }
  };

  if (loading) return <div>Loading model data...</div>;

  return (
    <div className="bg-white p-6 rounded-lg shadow border max-w-4xl">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-semibold text-gray-800">Model Management</h3>
        <button 
          onClick={handleRetrain} 
          disabled={retraining}
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 disabled:opacity-50"
        >
          {retraining ? 'Retraining...' : 'Retrain Model'}
        </button>
      </div>

      {message && <div className="mb-4 p-3 bg-blue-50 text-blue-800 rounded">{message}</div>}

      {modelData && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <h4 className="font-semibold text-gray-700 border-b pb-2">Model Information</h4>
            <div className="grid grid-cols-2 gap-y-3 text-sm">
              <span className="text-gray-500">Model Name:</span>
              <span className="font-medium">CustomerChurnPredictor</span>
              <span className="text-gray-500">Version:</span>
              <span className="font-medium">{modelData.version}</span>
              <span className="text-gray-500">Training Date:</span>
              <span className="font-medium">{new Date(modelData.created_at).toLocaleString()}</span>
              <span className="text-gray-500">Training Records:</span>
              <span className="font-medium">{modelData.training_records?.toLocaleString() || 'Unknown'}</span>
            </div>
          </div>

          <div className="space-y-4">
            <h4 className="font-semibold text-gray-700 border-b pb-2">Performance Metrics</h4>
            <div className="grid grid-cols-2 gap-y-3 text-sm">
              <span className="text-gray-500">Accuracy:</span>
              <span className="font-medium text-green-600">{(modelData.accuracy * 100).toFixed(1)}%</span>
              <span className="text-gray-500">Precision:</span>
              <span className="font-medium">{(modelData.precision * 100).toFixed(1)}%</span>
              <span className="text-gray-500">Recall:</span>
              <span className="font-medium">{(modelData.recall * 100).toFixed(1)}%</span>
              <span className="text-gray-500">F1 Score:</span>
              <span className="font-medium">{(modelData.f1_score * 100).toFixed(1)}%</span>
              <span className="text-gray-500">ROC-AUC:</span>
              <span className="font-medium">{(modelData.roc_auc * 100).toFixed(1)}%</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ModelAdmin;
