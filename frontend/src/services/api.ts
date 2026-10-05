import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

export const getHealth = () => api.get('/health');
export const getAnalyticsOverview = () => api.get('/analytics/overview');
export const getAnalyticsCharts = () => api.get('/analytics/charts');
export const getCustomers = (params: any) => api.get('/customers', { params });
export const predictSingle = (data: any) => api.post('/predict', data);
export const predictBatch = (formData: FormData) => api.post('/predict/batch', formData);

export default api;
