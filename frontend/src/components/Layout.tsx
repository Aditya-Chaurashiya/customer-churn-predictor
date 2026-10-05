import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

const Layout = () => {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b px-6 py-4 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-800">Customer Churn Intelligence</h2>
          <div className="flex items-center space-x-4 text-sm text-gray-600">
            <span>Model: <span className="font-medium text-gray-900">v1.0.0</span></span>
            <span>Dataset: <span className="font-medium text-gray-900">IBM Telco Churn</span></span>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
