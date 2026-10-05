import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { LayoutDashboard, Users, Activity, Settings, Database } from 'lucide-react';

const Sidebar = () => {
  const links = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/customers', label: 'Customers', icon: Users },
    { to: '/predict', label: 'Predict', icon: Activity },
    { to: '/model', label: 'Model', icon: Database },
  ];

  return (
    <div className="w-64 bg-gray-900 text-white min-h-screen flex flex-col">
      <div className="p-4 flex items-center border-b border-gray-800">
        <h1 className="text-xl font-bold text-indigo-400">ChurnPredictor</h1>
      </div>
      <nav className="flex-1 py-4">
        <ul>
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <li key={link.to}>
                <NavLink
                  to={link.to}
                  className={({ isActive }) =>
                    `flex items-center px-6 py-3 text-sm transition-colors ${
                      isActive ? 'bg-gray-800 text-white border-r-4 border-indigo-500' : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                    }`
                  }
                >
                  <Icon className="w-5 h-5 mr-3" />
                  {link.label}
                </NavLink>
              </li>
            );
          })}
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
