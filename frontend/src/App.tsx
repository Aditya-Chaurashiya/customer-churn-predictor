import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import Predict from './pages/Predict';
import ModelAdmin from './pages/ModelAdmin';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="customers" element={<Customers />} />
        <Route path="predict" element={<Predict />} />
        <Route path="model" element={<ModelAdmin />} />
      </Route>
    </Routes>
  );
}

export default App;
