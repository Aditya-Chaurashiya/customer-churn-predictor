import React, { useEffect, useState } from 'react';
import { getAnalyticsOverview, getAnalyticsCharts } from '../services/api';
import { 
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts';
import { Users, AlertTriangle, Activity, AlertCircle, Percent, Target } from 'lucide-react';

const COLORS = ['#4f46e5', '#ef4444', '#f59e0b', '#10b981'];
const RISK_COLORS = {
  'Low Risk': '#10b981',
  'Medium Risk': '#f59e0b',
  'High Risk': '#f97316',
  'Critical Risk': '#ef4444'
};

const Dashboard = () => {
  const [overview, setOverview] = useState<any>(null);
  const [charts, setCharts] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewRes, chartsRes] = await Promise.all([
          getAnalyticsOverview(),
          getAnalyticsCharts()
        ]);
        setOverview(overviewRes.data);
        setCharts(chartsRes.data);
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="flex justify-center items-center h-full">Loading analytics...</div>;
  if (error) return <div className="text-red-500 text-center">{error}</div>;
  if (!overview) return null;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <StatCard icon={Users} title="Total Customers" value={overview.total_customers.toLocaleString()} color="text-blue-500" />
        <StatCard icon={AlertTriangle} title="Predicted Churn" value={overview.predicted_churn.toLocaleString()} color="text-red-500" />
        <StatCard icon={AlertCircle} title="High Risk" value={overview.high_risk.toLocaleString()} color="text-orange-500" />
        <StatCard icon={Activity} title="Critical Risk" value={overview.critical_risk.toLocaleString()} color="text-red-600" />
        <StatCard icon={Percent} title="Avg Probability" value={`${(overview.average_probability * 100).toFixed(1)}%`} color="text-indigo-500" />
        <StatCard icon={Target} title="Model Accuracy" value={`${(overview.model_accuracy * 100).toFixed(1)}%`} color="text-green-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow border">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">Risk Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={charts?.risk_distribution || []}
                  cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value"
                >
                  {charts?.risk_distribution?.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={RISK_COLORS[entry.name as keyof typeof RISK_COLORS] || COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow border">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">Churn by Contract Type</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={charts?.contract_distribution || []} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#4f46e5" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon: Icon, title, value, color }: any) => (
  <div className="bg-white p-4 rounded-lg shadow border flex items-center space-x-4">
    <div className={`p-3 rounded-full bg-gray-50 ${color}`}>
      <Icon className="w-6 h-6" />
    </div>
    <div>
      <p className="text-sm text-gray-500 font-medium">{title}</p>
      <p className="text-xl font-bold text-gray-900">{value}</p>
    </div>
  </div>
);

export default Dashboard;
