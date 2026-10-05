import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { fetchCustomer } from '../services/api';
import RiskBadge from '../components/RiskBadge';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { CustomerWithPrediction } from '../types';

export default function CustomerDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [customer, setCustomer] = useState<CustomerWithPrediction | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadCustomer = async () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const data = await fetchCustomer(id);
      setCustomer(data);
    } catch (err) {
      setError('Customer not found or failed to load.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCustomer();
  }, [id]);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} onRetry={loadCustomer} />;
  if (!customer) return null;

  return (
    <div className="max-w-5xl mx-auto">
      <button onClick={() => navigate(-1)} className="flex items-center text-blue-600 hover:text-blue-800 mb-6">
        <ArrowLeft size={16} className="mr-2" /> Back to Customers
      </button>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden mb-6">
        <div className="p-6 border-b border-gray-200 flex justify-between items-center bg-gray-50">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Customer {customer.customer_id}</h1>
            <p className="text-gray-500 mt-1">Tenure: {customer.tenure} months</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <div className="text-sm text-gray-500">Churn Risk</div>
              <div className="text-xl font-bold text-gray-900">{(customer.churn_probability * 100).toFixed(1)}%</div>
            </div>
            <RiskBadge level={customer.risk_level} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
          {/* Prediction Info */}
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium mb-3">AI Prediction</h3>
              <div className="p-4 bg-slate-50 rounded-lg border border-slate-200">
                <p className="text-slate-800">{customer.prediction}</p>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-3 text-red-600">Risk Factors</h3>
              <ul className="list-disc pl-5 space-y-1 text-slate-700">
                {customer.risk_factors?.map((f, i) => <li key={i}>{f}</li>)}
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-3 text-green-600">Protective Factors</h3>
              <ul className="list-disc pl-5 space-y-1 text-slate-700">
                {customer.protective_factors?.map((f, i) => <li key={i}>{f}</li>)}
              </ul>
            </div>
          </div>

          {/* Customer Profile */}
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium mb-3">Service Details</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div><span className="text-gray-500 block">Contract</span> <span className="font-medium">{customer.contract}</span></div>
                <div><span className="text-gray-500 block">Internet Service</span> <span className="font-medium">{customer.internet_service || 'No'}</span></div>
                <div><span className="text-gray-500 block">Monthly Charges</span> <span className="font-medium">${customer.monthly_charges.toFixed(2)}</span></div>
                <div><span className="text-gray-500 block">Total Charges</span> <span className="font-medium">${customer.total_charges?.toFixed(2) || '0.00'}</span></div>
                <div><span className="text-gray-500 block">Payment Method</span> <span className="font-medium">{customer.payment_method}</span></div>
                <div><span className="text-gray-500 block">Paperless Billing</span> <span className="font-medium">{customer.paperless_billing}</span></div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-medium mb-3">Demographics</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div><span className="text-gray-500 block">Gender</span> <span className="font-medium">{customer.gender}</span></div>
                <div><span className="text-gray-500 block">Senior Citizen</span> <span className="font-medium">{customer.senior_citizen ? 'Yes' : 'No'}</span></div>
                <div><span className="text-gray-500 block">Partner</span> <span className="font-medium">{customer.partner}</span></div>
                <div><span className="text-gray-500 block">Dependents</span> <span className="font-medium">{customer.dependents}</span></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
