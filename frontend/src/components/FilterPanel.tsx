import React from 'react';

export default function FilterPanel() {
  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 mb-6 flex flex-wrap gap-4">
      <div className="flex-1 min-w-[200px]">
        <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
        <input type="text" placeholder="Search customers..." className="w-full border-gray-300 rounded-md shadow-sm border p-2" />
      </div>
      <div className="flex-1 min-w-[150px]">
        <label className="block text-sm font-medium text-gray-700 mb-1">Risk Level</label>
        <select className="w-full border-gray-300 rounded-md shadow-sm border p-2">
          <option value="">All</option>
          <option value="Critical">Critical</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>
      <div className="flex-1 min-w-[150px]">
        <label className="block text-sm font-medium text-gray-700 mb-1">Contract</label>
        <select className="w-full border-gray-300 rounded-md shadow-sm border p-2">
          <option value="">All</option>
          <option value="Month-to-month">Month-to-month</option>
          <option value="One year">One year</option>
          <option value="Two year">Two year</option>
        </select>
      </div>
      <div className="flex items-end">
        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Apply Filters</button>
      </div>
    </div>
  );
}
