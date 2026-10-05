import React, { useEffect, useState } from 'react';
import { getCustomers } from '../services/api';
import { Search, Filter, ChevronLeft, ChevronRight } from 'lucide-react';
import clsx from 'clsx';

const Customers = () => {
  const [data, setData] = useState<any[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  
  const [riskFilter, setRiskFilter] = useState('');
  
  const fetchCustomers = async (p: number, risk: string) => {
    setLoading(true);
    try {
      const res = await getCustomers({ page: p, limit: 20, risk: risk || undefined });
      setData(res.data.data);
      setTotal(res.data.total);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomers(page, riskFilter);
  }, [page, riskFilter]);

  const totalPages = Math.ceil(total / 20);

  const getRiskBadge = (risk: string) => {
    const colors: Record<string, string> = {
      'Critical Risk': 'bg-red-100 text-red-800 border-red-200',
      'High Risk': 'bg-orange-100 text-orange-800 border-orange-200',
      'Medium Risk': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'Low Risk': 'bg-green-100 text-green-800 border-green-200'
    };
    const style = colors[risk] || 'bg-gray-100 text-gray-800 border-gray-200';
    return <span className={clsx("px-2.5 py-0.5 rounded-full text-xs font-medium border", style)}>{risk}</span>;
  };

  return (
    <div className="bg-white rounded-lg shadow border flex flex-col h-full">
      <div className="p-4 border-b flex justify-between items-center bg-gray-50 rounded-t-lg">
        <h3 className="font-semibold text-gray-800">High-Risk Customers Table</h3>
        
        <div className="flex space-x-2">
          <div className="relative">
            <select 
              value={riskFilter}
              onChange={(e) => { setRiskFilter(e.target.value); setPage(1); }}
              className="pl-8 pr-4 py-2 border rounded-md text-sm bg-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="">All Risks</option>
              <option value="Critical Risk">Critical Risk</option>
              <option value="High Risk">High Risk</option>
              <option value="Medium Risk">Medium Risk</option>
              <option value="Low Risk">Low Risk</option>
            </select>
            <Filter className="w-4 h-4 text-gray-400 absolute left-2.5 top-2.5" />
          </div>
        </div>
      </div>
      
      <div className="flex-1 overflow-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50 sticky top-0">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contract</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tenure</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Monthly Charges</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Probability</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Risk Level</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {loading ? (
              <tr><td colSpan={6} className="text-center py-10 text-gray-500">Loading...</td></tr>
            ) : data.length === 0 ? (
              <tr><td colSpan={6} className="text-center py-10 text-gray-500">No customers found</td></tr>
            ) : (
              data.map((row, i) => (
                <tr key={i} className="hover:bg-gray-50 cursor-pointer">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-indigo-600">{row.customer_id}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{row.contract}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{row.tenure} mo</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${row.monthly_charges.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-medium">
                    {row.churn_probability ? `${(row.churn_probability * 100).toFixed(1)}%` : 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getRiskBadge(row.risk)}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      
      <div className="p-4 border-t flex justify-between items-center bg-gray-50 rounded-b-lg text-sm text-gray-600">
        <div>
          Showing {((page - 1) * 20) + 1} to {Math.min(page * 20, total)} of {total} results
        </div>
        <div className="flex space-x-2">
          <button 
            disabled={page === 1}
            onClick={() => setPage(p => Math.max(1, p - 1))}
            className="p-1 border rounded bg-white disabled:opacity-50 hover:bg-gray-100"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button 
            disabled={page >= totalPages}
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            className="p-1 border rounded bg-white disabled:opacity-50 hover:bg-gray-100"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Customers;
