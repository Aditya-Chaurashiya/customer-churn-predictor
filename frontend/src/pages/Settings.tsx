import React from 'react';

export default function Settings() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-500 mt-1">Configure application parameters.</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 max-w-2xl">
        <h3 className="text-lg font-medium mb-4">Risk Thresholds</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Critical Risk Threshold (%)</label>
            <input type="number" defaultValue={70} className="mt-1 block w-full rounded-md border-gray-300 border p-2 shadow-sm" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">High Risk Threshold (%)</label>
            <input type="number" defaultValue={40} className="mt-1 block w-full rounded-md border-gray-300 border p-2 shadow-sm" />
          </div>
        </div>

        <h3 className="text-lg font-medium mb-4 mt-8">System Status</h3>
        <div className="space-y-3 text-sm">
          <div className="flex justify-between border-b pb-2"><span className="text-gray-500">API Connection</span><span className="font-medium text-green-600">Connected</span></div>
          <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Database</span><span className="font-medium text-green-600">Healthy</span></div>
          <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Version</span><span className="font-medium">1.0.0</span></div>
        </div>

        <div className="mt-8">
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Save Configuration</button>
        </div>
      </div>
    </div>
  );
}
