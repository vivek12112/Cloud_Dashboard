import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });
        
        localStorage.setItem('access_token', response.data.access);
        api.defaults.headers.Authorization = `Bearer ${response.data.access}`;
        
        return api(originalRequest);
      } catch (err) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(err);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;

// Auth APIs
export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (userData) => api.post('/auth/register/', userData),
  getCurrentUser: () => api.get('/auth/me/'),
  getUsers: () => api.get('/auth/users/'),
  updateUserRole: (userId, role) => api.patch(`/auth/users/${userId}/role/`, { role }),
};

// Resources APIs
export const resourcesAPI = {
  getAll: () => api.get('/resources/'),
  getById: (id) => api.get(`/resources/${id}/`),
  create: (data) => api.post('/resources/', data),
  update: (id, data) => api.patch(`/resources/${id}/`, data),
  delete: (id) => api.delete(`/resources/${id}/`),
  start: (id) => api.post(`/resources/${id}/start/`),
  stop: (id) => api.post(`/resources/${id}/stop/`),
  approve: (id) => api.post(`/resources/${id}/approve/`),
};

// Monitoring APIs
export const monitoringAPI = {
  getMetrics: () => api.get('/monitoring/metrics/'),
  getAlerts: () => api.get('/monitoring/alerts/'),
  getDashboardStats: () => api.get('/monitoring/dashboard-stats/'),
  generateMockMetrics: (resourceId) => api.post('/monitoring/generate-metrics/', { resource_id: resourceId }),
};

// Billing APIs
export const billingAPI = {
  getRecords: () => api.get('/billing/records/'),
  getBudgets: () => api.get('/billing/budgets/'),
  createBudget: (data) => api.post('/billing/budgets/', data),
  getSummary: () => api.get('/billing/summary/'),
  generateMockBilling: (resourceId) => api.post('/billing/generate-mock/', { resource_id: resourceId }),
};

// Support APIs
export const supportAPI = {
  getTickets: () => api.get('/support/tickets/'),
  createTicket: (data) => api.post('/support/tickets/', data),
  updateTicket: (id, data) => api.patch(`/support/tickets/${id}/`, data),
};

// Network APIs
export const networkAPI = {
  getPolicies: () => api.get('/network/policies/'),
  createPolicy: (data) => api.post('/network/policies/', data),
  getFirewallRules: () => api.get('/network/firewall-rules/'),
  createFirewallRule: (data) => api.post('/network/firewall-rules/', data),
};
