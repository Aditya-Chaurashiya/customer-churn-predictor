import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer } from 'recharts';
import { fetchChurnByService, fetchChurnByCharges } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

export default function Analytics() {
  const [loading, setLoading] = useState(true);
  const [serviceData, setServiceData] = useState<any[]>([]);
  const [chargesData, setChargesData] = useState<any[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const [sv, ch] = await Promise.all([
          fetchChurnByService(),
          fetchChurnByCharges()
        ]);
        setServiceData(sv);
        setChargesData(ch);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Advanced Analytics</h1>
        <p className="text-gray-500 mt-1">Deep dive into customer churn indicators.</p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-96">
          <h3 className="text-lg font-medium mb-4">Churn by Internet Service</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={serviceData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="service_type" />
              <YAxis />
              <RechartsTooltip />
              <Legend />
              <Bar dataKey="churned" stackId="a" fill="#ef4444" name="Churned" />
              <Bar dataKey="total" stackId="a" fill="#3b82f6" name="Retained" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-96">
          <h3 className="text-lg font-medium mb-4">Churn by Monthly Charges</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chargesData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="charge_range" />
              <YAxis />
              <RechartsTooltip />
              <Legend />
              <Bar dataKey="churned" stackId="a" fill="#ef4444" name="Churned" />
              <Bar dataKey="total" stackId="a" fill="#3b82f6" name="Retained" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
